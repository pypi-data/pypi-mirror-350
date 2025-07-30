import json
import logging
import time
import urllib.parse as urlparse

import requests
from scrapy.exceptions import NotConfigured


class ProxyServerNotAvailable(Exception):
    def __init__(self, proxy_address):
        self.proxy_address = proxy_address
        self.message = "Proxy server is not available"
        super().__init__()

    def __str__(self):
        return f'{self.proxy_address} -> {self.message}'


class ProxyAuthorizationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()

    def __str__(self):
        return self.message


class ArgumentsException(Exception):
    def __init__(self):
        self.message = "No required arguments. To use proxy need: proxypy_url, proxypy_api_login, proxypy_api_key"
        super().__init__()

    def __str__(self):
        return self.message


logger = logging.getLogger(__name__)


class ProxyPyDownloaderMiddleware:
    def __init__(self, proxy_settings):
        connect_key_set = {
            "use_proxy",
            "proxypy_url",
            "proxypy_api_login",
            "proxypy_api_key",
            "proxypy_health_check_retry_times",
            "proxypy_health_check_retry_interval"
        }
        for key in connect_key_set:
            setattr(self, key, proxy_settings[key])
        if self.use_proxy:
            if not (self.proxypy_url and self.proxypy_api_login and self.proxypy_api_key):
                raise ArgumentsException()
            self.request_settings = {key: value for key, value in proxy_settings.items() if key not in connect_key_set}
            parsed_proxypy_url = urlparse.urlparse(self.proxypy_url)
            self.proxy_url_template = f"{parsed_proxypy_url.scheme}://{self.proxypy_api_login}:{{encoded_settings}}" \
                                      f"@{parsed_proxypy_url.netloc}"
            self.health_check()
        else:
            raise NotConfigured()

    def make_proxy_url(self, **request_settings):
        settings = {"proxypy_api_key": self.proxypy_api_key, **request_settings}
        encoded_settings = urlparse.quote(json.dumps(settings))
        return self.proxy_url_template.format(encoded_settings=encoded_settings)

    def health_check(self):
        tries = 0
        while True:
            try:
                # health_check contains test url, it doesn't matter what url we use, because in health-check
                # proxypy-server will give his response to us and not went to request url
                health_check = requests.get(url="http://test.ru",
                                            headers={"health_check": "health_check"},
                                            timeout=60,
                                            proxies={"http": self.make_proxy_url()})
                break
            except requests.exceptions.RequestException:
                tries += 1
                logger.info(f"Proxy server connection failed {tries}/{self.proxypy_health_check_retry_times} times")
                if tries < self.proxypy_health_check_retry_times:
                    logger.info(f"Sleeping for {self.proxypy_health_check_retry_interval} seconds")
                    time.sleep(self.proxypy_health_check_retry_interval)  # intentionally blocks twisted loop
                else:
                    raise ProxyServerNotAvailable(proxy_address=self.proxypy_url)
        if not health_check.ok:
            raise ProxyAuthorizationError(message=health_check.text)
        logger.info("Proxy server is available. Authorization is successful")

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        proxy_settings = {
            'use_proxy': settings.getbool('USE_PROXY', False),

            'proxypy_url': settings.get('PROXYPY_URL', None),
            'proxypy_api_key': settings.get('PROXYPY_API_KEY', None),
            'proxypy_api_login': settings.get('PROXYPY_API_LOGIN', None),

            'proxypy_health_check_retry_times': settings.getint('PROXYPY_HEALTH_CHECK_RETRY_TIMES', 15),
            'proxypy_health_check_retry_interval': settings.getint('PROXYPY_HEALTH_CHECK_RETRY_INTERVAL', 60),

            'proxypy_tor': settings.get('PROXYPY_TOR', None),
            'proxypy_country': settings.get('PROXYPY_COUNTRY', None),
            'proxypy_ignore_country': settings.get('PROXYPY_IGNORE_COUNTRY', None),
            'proxypy_fastest': settings.getbool('PROXYPY_FASTEST', False)
        }
        return cls(proxy_settings)

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            return
        if not request.meta.get('use_proxy', self.use_proxy):
            return
        request_settings = {key: request.meta.get(key, default)
                            for key, default in self.request_settings.items()}
        request.meta['proxy'] = self.make_proxy_url(**request_settings)
