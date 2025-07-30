import json
import types
import warnings
from datetime import datetime, timezone

from itemadapter import ItemAdapter
from scrapy.crawler import Crawler
from scrapy.exceptions import ScrapyDeprecationWarning

from crawler_utils.opensearch.storage import OpenSearchStorage
from crawler_utils.talisman_job_env import TalismanJobEnvironment
from crawler_utils.timestamp import ensure_seconds


class OpenSearchItemsPipeline:
    """
    OpenSearch items pipeline.

    Settings:
    `OPENSEARCH_ITEMS_SETTINGS` - dict specifying OpenSearch client connections:
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

    `OPENSEARCH_ITEMS_INDEX`: Optional[str] = "scrapy-job-items" - index in OpenSearch.
    """

    def __init__(self, os_storage: OpenSearchStorage, index, job_id):
        self.os_storage = os_storage
        self.index = index
        self.job_id = job_id

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        if crawler.settings.getdict("ELASTICSEARCH_ITEMS_SETTINGS") is not None:
            warnings.warn(
                "`ELASTICSEARCH_ITEMS_SETTINGS` is deprecated, "
                "use `OPENSEARCH_ITEMS_SETTINGS` instead.",
                ScrapyDeprecationWarning,
                stacklevel=2,
            )
            os_settings = crawler.settings.getdict("ELASTICSEARCH_ITEMS_SETTINGS")
        else:
            os_settings = crawler.settings.getdict("OPENSEARCH_ITEMS_SETTINGS")
        os_storage = OpenSearchStorage.from_settings(os_settings)
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        return cls(
            os_storage,
            index=crawler.settings.get("OPENSEARCH_ITEMS_INDEX", "scrapy-job-items"),
            job_id=job_env.job_id,
        )

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):  # Sequence?
            for each in item:
                self.process_item(each, spider)
        else:
            indexed_item = ItemAdapter(item).asdict()
            if self.job_id:
                indexed_item["job_id"] = self.job_id

            timestamp = item.get("_timestamp", None)
            if isinstance(timestamp, str):
                ts = timestamp
            elif isinstance(timestamp, int):
                ts = datetime.fromtimestamp(
                    ensure_seconds(timestamp), tz=timezone.utc
                ).isoformat()
            else:
                ts = datetime.now().isoformat()

            indexed_item = {
                "@timestamp": ts,
                "job_id": self.job_id if self.job_id else None,
                "_url": item.get("_url", None),
                "_uuid": item.get("_uuid", None),
                "_attachments": item.get("_attachments", None),
                "item": json.dumps(item),
            }

            self.os_storage.index_item(self.index, indexed_item)
        return item

    def close_spider(self, spider):
        self.os_storage.close()
