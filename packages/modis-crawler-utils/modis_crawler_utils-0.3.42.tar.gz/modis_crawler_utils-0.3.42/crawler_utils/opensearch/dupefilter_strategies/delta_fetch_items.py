import warnings
from datetime import datetime
from typing import Optional

from scrapy import Request, signals
from scrapy.exceptions import ScrapyDeprecationWarning

from crawler_utils.opensearch.dupefilter_strategies import (
    OpenSearchDupeFilterStrategy,
)
from crawler_utils.opensearch.request_fingerprint import default_request_fingerprint
from crawler_utils.opensearch.storage import (
    OpenSearchStorage,
    OpenSearchStorageLoader,
)
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class FingerprintSet:
    def __init__(self):
        self._seen = set()
        self._batch = []

    def add(self, fp):
        if fp in self._seen:
            return False
        self._seen.add(fp)
        self._batch.append(fp)
        return True

    def pop_batch(self):
        batch = self._batch
        self._batch = []
        return batch

    def batch_length(self):
        return len(self._batch)


class DeltaFetchItemsStrategy(OpenSearchDupeFilterStrategy):
    def __init__(
        self,
        os_storage: OpenSearchStorage,
        index: str,
        job_env: TalismanJobEnvironment = None,
        requests_update_batch_size: int = 100,
    ):
        self.os_storage = os_storage
        self.index = index
        self.job_env = job_env or TalismanJobEnvironment()
        self.requests_update_batch_size = requests_update_batch_size
        self._requests_with_items = FingerprintSet()
        self._job_start_time = datetime.now().isoformat()

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
        strategy = cls(os_storage, index, job_env)
        crawler.signals.connect(strategy.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(strategy.close_spider, signal=signals.spider_closed)
        return strategy

    def query(self, request: Request) -> Optional[dict]:
        return {"match": {"has_items": True}}

    @staticmethod
    def request_fingerprint(request):
        return default_request_fingerprint(request).hex()

    def item_scraped(self, item, response, spider):
        if response.meta.get("_has_items"):
            return
        response.meta["_has_items"] = True

        request_fp = self.request_fingerprint(response.request)
        if not self._requests_with_items.add(request_fp):
            return
        if self._requests_with_items.batch_length() < self.requests_update_batch_size:
            return
        self._update_requests_with_items()

    def _update_requests_with_items(self):
        self._mark_requests_in_base(self._requests_with_items.pop_batch())

    def _mark_requests_in_base(self, fingerprints, mark="has_items"):
        if not fingerprints:
            return

        if self.os_storage.has_pending_items():
            self.os_storage.send_items(refresh="wait_for")
        else:
            self.os_storage.refresh_index(self.index)

        queries = [{"match": {"fingerprint": " ".join(fingerprints)}}]
        if self.job_env.job_id:
            queries.append({"match": {"job_id": self.job_env.job_id}})
        else:
            queries.append({"range": {"@timestamp": {"gte": self._job_start_time}}})

        self.os_storage.update_by_query(
            f"{self.index},{self.index}-*",
            query={"bool": {"must": queries}},
            script=f"ctx._source.{mark} = true",
        )

    def close_spider(self, spider):
        self._update_requests_with_items()
        self.os_storage.close()
