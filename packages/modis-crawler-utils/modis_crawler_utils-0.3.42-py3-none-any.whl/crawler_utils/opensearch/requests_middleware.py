import time
import warnings
from datetime import datetime

from scrapy import signals
from scrapy.exceptions import ScrapyDeprecationWarning

from crawler_utils.opensearch.request_fingerprint import default_request_fingerprint
from crawler_utils.opensearch.storage import (
    OpenSearchStorage,
    OpenSearchStorageLoader,
)
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class OpenSearchRequestsDownloaderMiddleware:
    """
    OpenSearchRequestsDownloaderMiddleware transforms request-response pair into an item,
    and then sends it to the OpenSearch.

    Settings:

    `OPENSEARCH_REQUESTS_SETTINGS` - dict specifying OpenSearch client connections:
        "hosts": Optional[str | list[str]] = "localhost:9200" - hosts with opensearch endpoint,
        "timeout": Optional[int] = 60 - timeout of connections,
        "http_auth": Optional[tuple[str, str]] = None - HTTP authentication if needed,
        "port": Optional[int] = 443 - access port if not specified in hosts,
        "use_ssl": Optional[bool] = True - usage of SSL,
        "verify_certs": Optional[bool] = False - verifying certificates,
        "ssl_show_warn": Optional[bool] = False - show SSL warnings,
        "ca_certs": Optional[str] = None - CA certificate path,
        "client_key": Optional[str] = None - client key path,
        "client_cert": Optional[str] = None - client certificate path,
        "buffer_length": Optional[int] = 500 - number of items in OpenSearchStorage's buffer.

    `OPENSEARCH_REQUESTS_INDEX`: Optional[str] = "scrapy-job-requests" - index in OpenSearch.
    """

    def __init__(
        self,
        os_storage: OpenSearchStorage,
        index: str,
        job_env: TalismanJobEnvironment = None,
    ):
        self.os_storage = os_storage
        self.index = index
        self.job_env = job_env or TalismanJobEnvironment()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        os_settings_key = "OPENSEARCH_REQUESTS_SETTINGS"
        if settings.get("ELASTICSEARCH_REQUESTS_SETTINGS") is not None:
            warnings.warn(
                "`ELASTICSEARCH_REQUESTS_SETTINGS` is deprecated. "
                "Use `OPENSEARCH_REQUESTS_SETTINGS` instead.",
                ScrapyDeprecationWarning,
                stacklevel=2,
            )
            os_settings_key = "ELASTICSEARCH_REQUESTS_SETTINGS"
        os_storage = OpenSearchStorageLoader.from_crawler(crawler, os_settings_key)
        index = crawler.settings.get("OPENSEARCH_REQUESTS_INDEX", "scrapy-job-requests")
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        middleware = cls(os_storage, index, job_env)
        crawler.signals.connect(middleware.close_spider, signal=signals.spider_closed)
        return middleware

    @staticmethod
    def process_request(request, spider):
        if not request.meta.get("dont_index"):
            request.meta["request_timer/start"] = time.time()

    def process_response(self, request, response, spider):
        if request.meta.get("dont_index") or "request_timer/start" not in request.meta:
            return response

        item = self._request2item(request)
        item.update(self._response2item(response))
        self.os_storage.index_item(self.index, item)

        return response

    def process_exception(self, request, exception, spider):
        if request.meta.get("dont_index") or "request_timer/start" not in request.meta:
            return
        item = self._request2item(request)
        self.os_storage.index_item(self.index, item)

    def _request2item(self, request) -> dict:
        timestamp = time.time()
        timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
        item = {
            "url": request.url,
            "request_url": request.url,
            "method": request.method,
            "fingerprint": self._request_fingerprint(request),
            "duration": int(timestamp - request.meta["request_timer/start"]),
            "last_seen": timestamp_iso,
            "@timestamp": timestamp_iso,
        }
        if self.job_env.job_id:
            item["job_id"] = self.job_env.job_id
        if self.job_env.crawler_id:
            item["crawler_id"] = self.job_env.crawler_id
        if self.job_env.version_id:
            item["version_id"] = int(
                self.job_env.version_id
            )  # int to enable sorting on
        if self.job_env.periodic_job_id:
            item["periodic_job_id"] = self.job_env.periodic_job_id
        return item

    @staticmethod
    def _response2item(response) -> dict:
        return {
            "url": response.url,
            "http_status": response.status,
            "response_size": len(response.body),
        }

    @staticmethod
    def _request_fingerprint(request):
        return default_request_fingerprint(request).hex()

    def close_spider(self, spider):
        self.os_storage.close()
