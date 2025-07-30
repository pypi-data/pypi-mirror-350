import dataclasses
import json
import logging
import typing
import urllib.parse as urlparse
import uuid
from copy import deepcopy

import requests
import time
from scrapy import Request
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

logger = logging.getLogger(__name__)

DEFAULT_PROXY_URL = 'http://proxy.talisman.ispras.ru:20718'
HEALTH_CHECK_URL = 'http://demo-site.at.ispras.ru'  # TODO


@dataclasses.dataclass
class TalismanProxyConfig:
    url: str
    login: str
    token: str = dataclasses.field(repr=False)
    id: str = None
    ignored_ids: list[str] = dataclasses.field(default_factory=list)
    use_tor: bool = False
    country: str = None
    ignored_countries: list[str] = dataclasses.field(default_factory=list)
    use_fastest: bool = False
    use_socks: bool = False

    def __post_init__(self):
        if not self.url:
            raise ValueError('Undefined talisman proxy url')
        if not self.login:
            raise ValueError('Undefined talisman proxy login')
        if not self.token:
            raise ValueError('Undefined talisman proxy token')

    @classmethod
    def from_settings(cls, settings: Settings):
        def resolve(key, proxypy_key=None, getter=settings.get):
            full_key = f'TALISMAN_PROXY_{key}'
            if full_key not in settings and proxypy_key:
                return getter(f'PROXYPY_{proxypy_key}')
            return getter(full_key)

        return cls(
            url=resolve('URL') or DEFAULT_PROXY_URL,
            login=resolve('LOGIN', proxypy_key='API_LOGIN'),
            token=resolve('TOKEN', proxypy_key='API_KEY'),
            id=resolve('ID'),
            ignored_ids=resolve('IGNORED_IDS', getter=settings.getlist),
            use_tor=resolve('USE_TOR', proxypy_key='TOR', getter=settings.getbool),
            country=resolve('COUNTRY', proxypy_key='COUNTRY'),
            ignored_countries=resolve('IGNORED_COUNTRIES', proxypy_key='IGNORE_COUNTRY', getter=settings.getlist),
            use_fastest=resolve('USE_FASTEST', proxypy_key='FASTEST', getter=settings.getbool),
            use_socks=resolve('USE_SOCKS', getter=settings.getbool)
        )

    @property
    def full_url(self):
        parsed_url = urlparse.urlparse(self.url)
        settings = {
            "token": self.token,
            "useTor": self.use_tor,
            "proxyId": self.id,
            "ignoredProxies": self.ignored_ids,
            "country": self.country,
            "ignoredCountries": self.ignored_countries,
            "useFastest": self.use_fastest,
            "useSocks": self.use_socks
        }
        encoded_settings = urlparse.quote(json.dumps(settings, separators=(',', ':')))
        return f'{parsed_url.scheme}://{self.login}:{encoded_settings}@{parsed_url.netloc}'


PartialProxyConfig = typing.Union[TalismanProxyConfig, typing.Dict[str, typing.Any]]


class TalismanProxyError(Exception):
    def __init__(self, config: TalismanProxyConfig, message: str):
        self.config = config
        super().__init__(message)


class ProxyServerNotAvailable(TalismanProxyError):
    def __init__(self, config: TalismanProxyConfig):
        super().__init__(config, f'Talisman proxy {config.url} is not available')


class ProxyHealthCheckError(TalismanProxyError):
    def __init__(self, config: TalismanProxyConfig, reason: str):
        super().__init__(config, f'Talisman proxy {config.url} check failed: {reason}')


def request_talisman_proxy_id(config: TalismanProxyConfig) -> int:
    response = requests.get(url=HEALTH_CHECK_URL,
                            headers={"X-Proxy-Chain-Health-Check": "1"},
                            timeout=60,
                            proxies={"http": config.full_url})
    if not response.ok:
        raise ProxyHealthCheckError(config, response.text)
    return response.json()['proxyId']


class TalismanProxyChainDownloaderMiddleware:
    """

    1. Using proxy

    When middleware is enabled and proxying is turned on (USE_PROXY = True or USE_TALISMAN_PROXY = True), all
    requests will be sent through our proxy server.

    All proxypy settings are supported:
    +----------------------------------+------------------------+---------------------------+
    | Talisman Proxy Setting           | Proxypy setting        | Description               |
    +----------------------------------+------------------------+---------------------------+
    | USE_TALISMAN_PROXY               | USE_PROXY              | Proxy requests by default |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_LOGIN             | PROXYPY_API_LOGIN      | Proxy login               |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_TOKEN             | PROXYPY_API_KEY        | Proxy access token        |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_ID                | -                      | Concrete proxy id         |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_IGNORED_IDS       | -                      | Proxy ids to ignore       |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_USE_TOR           | PROXYPY_TOR            | Use tor proxy             |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_COUNTRY           | PROXYPY_COUNTRY        | Use proxy from country    |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_IGNORED_COUNTRIES | PROXYPY_IGNORE_COUNTRY | Country codes to ignore   |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_USE_FASTEST       | PROXYPY_FASTEST        | Use fastest proxies       |
    +----------------------------------+------------------------+---------------------------+
    | TALISMAN_PROXY_USE_SOCKS         | -                      | Use socks proxies         |
    +----------------------------------+------------------------+---------------------------+

    1.1. Override proxy selection parameters per request

    request.meta['talisman_proxy_config'] = {
        'country': 'us'
    }

    1.2. Bypass proxy

    request.meta['use_proxy'] = False
    or
    request.meta['proxy'] = None


    2. Using sessions

    Sessions allow to send a number of requests through the same internal proxy.

    2.1. Use single session for all requests

    TALISMAN_PROXY_USE_DEFAULT_SESSION = True

    Session params are inferred from other settings.

    2.2. Proxy request without session

    request.meta['talisman_proxy_session'] = None

    2.3. Send different requests in different sessions

    request1.meta['talisman_proxy_session'] = 'session_key_1'
    request2.meta['talisman_proxy_session'] = 'session_key_2'

    Session is created on the first request with given key.

    2.4. Managing sessions explicitly from spider

    session_key = self.crawler.talisman_proxy.create_session()
    yield Request('...', meta={'talisman_proxy_session': session_key})
    ...
    # providing custom key and override default configuration
    self.crawler.talisman_proxy.create_session(
        session_key='my awesome key',
        config={
            'country': 'us'
        }
    )
    yield Request('...', meta={'talisman_proxy_session': 'my awesome key'})
    ...
    self.crawler.talisman_proxy.rotate_session(session_key)  # change proxy
    self.crawler.talisman_proxy.close_session(session_key)  # remove

    2.5 Autorotation

    Proxy sessions will rotate automatically on certain HTTP responses.
    When a request through session results in HTTP code specified by TALISMAN_PROXY_ROTATE_SESSION_ON_HTTP_CODES
    setting, middleware will try to change session's proxy and retry this request.
    Default rotation codes are 502 and 504.

    The request will be retried at max TALISMAN_PROXY_ROTATE_MAX_RETRIES times, default is 3.

    # TODO session op errors, exclusive sessions, backoffs, etc

    """

    def __init__(self,
                 proxy_config: TalismanProxyConfig,
                 health_check_retry_times: int,
                 health_check_retry_interval: int,
                 use_default_session: bool,
                 rotate_session_on_http_codes: list[int],
                 rotate_session_max_retries: int):
        self.proxy_config = proxy_config
        self.health_check_retry_times = health_check_retry_times
        self.health_check_retry_interval = health_check_retry_interval
        self.use_default_session = use_default_session
        self.rotate_session_on_http_codes = list(map(int, rotate_session_on_http_codes))
        self.rotate_session_max_retries = rotate_session_max_retries

        self.health_check()

        self._default_session_key = None
        self._session_configs = {}  # key -> config
        if self.use_default_session:
            self._default_session_key = self.create_session()

    def health_check(self):
        tries = 0
        while True:
            try:
                request_talisman_proxy_id(self.proxy_config)
                break
            except requests.exceptions.RequestException:
                tries += 1
                logger.info(f"Proxy server connection failed {tries}/{self.health_check_retry_times} times")
                if tries < self.health_check_retry_times:
                    logger.info(f"Sleeping for {self.health_check_retry_interval} seconds")
                    time.sleep(self.health_check_retry_interval)  # intentionally blocks twisted loop
                else:
                    raise ProxyServerNotAvailable(self.proxy_config)
            except ProxyHealthCheckError:
                raise
        logger.info("Proxy server is available. Authorization is successful")

    @classmethod
    def from_crawler(cls, crawler):
        if proxy_mw := getattr(crawler, 'talisman_proxy', None):
            return proxy_mw
        settings = crawler.settings

        if not settings.getbool('USE_TALISMAN_PROXY') and not settings.getbool('USE_PROXY'):
            raise NotConfigured()

        crawler.talisman_proxy = cls(
            proxy_config=TalismanProxyConfig.from_settings(settings),
            health_check_retry_times=settings.getint('TALISMAN_PROXY_HEALTH_CHECK_RETRY_TIMES', 15),
            health_check_retry_interval=settings.getint('TALISMAN_PROXY_HEALTH_CHECK_RETRY_INTERVAL', 60),
            use_default_session=settings.getbool('TALISMAN_PROXY_USE_DEFAULT_SESSION'),
            rotate_session_on_http_codes=settings.getlist('TALISMAN_PROXY_ROTATE_SESSION_ON_HTTP_CODES', [502, 504]),
            rotate_session_max_retries=settings.getint('TALISMAN_PROXY_ROTATE_MAX_RETRIES', 3)
        )
        return crawler.talisman_proxy

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            return

        if not request.meta.get('use_proxy', True):
            return

        request_proxy_config = request.meta.get('talisman_proxy_config')
        if session_key := self._get_session_key(request):
            if not self.session_exists(session_key):
                self.create_session(session_key, request_proxy_config)
            request_proxy_config = self.get_session_config(session_key)
        else:
            request_proxy_config = self._get_complete_config(request_proxy_config)
        request.meta['proxy'] = request_proxy_config.full_url

    def _get_session_key(self, request: Request) -> typing.Optional[str]:
        return request.meta.get('talisman_proxy_session', self._default_session_key)

    def _get_complete_config(self, config: PartialProxyConfig = None) -> TalismanProxyConfig:
        if config is None:
            return self.proxy_config
        if isinstance(config, TalismanProxyConfig):
            return config
        if isinstance(config, dict):
            return dataclasses.replace(self.proxy_config, **config)
        raise TypeError(f'Invalid proxy configuration type {type(config)}')

    def process_response(self, request, response, spider):
        if not request.meta.get('proxy'):
            return response

        if not (session_key := self._get_session_key(request)):
            return response

        if response.status not in self.rotate_session_on_http_codes:
            return response

        self.rotate_session(session_key)
        return self._retry(request, f'{response.status} {response.text}') or response

    def _retry(self, request, reason):
        if (retries := request.meta.get('talisman_proxy_retries', 0)) < self.rotate_session_max_retries:
            logger.debug(f'Retrying request {request} with different proxy '
                         f'({retries + 1}/{self.rotate_session_max_retries} times): {reason}')
            retry_request = request.replace(dont_filter=True)
            retry_request.meta['talisman_proxy_retries'] = retries + 1
            del retry_request.meta['proxy']
            return retry_request
        logger.warning(f'Gave up retrying request {request} with different proxies '
                       f'(failed {self.rotate_session_max_retries} times): {reason}')
        return None

    @staticmethod
    def generate_session_key() -> str:
        return str(uuid.uuid4())

    def get_session_config(self, session_key: str) -> typing.Optional[TalismanProxyConfig]:
        return self._session_configs.get(session_key)

    def session_exists(self, session_key: str) -> bool:
        return session_key in self._session_configs

    def create_session(self,
                       session_key: str = None,
                       config: PartialProxyConfig = None) -> str:
        if not session_key:
            session_key = self.generate_session_key()
        config = deepcopy(self._get_complete_config(config))
        if not config.id:
            config.id = request_talisman_proxy_id(config)
        self._session_configs[session_key] = config
        return session_key

    def rotate_session(self, session_key: str):
        if not (config := self._session_configs.get(session_key)):
            raise ValueError(f'There is no proxy session with key {session_key}')
        if config.id and config.id not in config.ignored_ids:
            config.ignored_ids.append(config.id)
        config.id = None
        config.id = request_talisman_proxy_id(config)

    def close_session(self, session_key: str):
        self._session_configs.pop(session_key, None)
