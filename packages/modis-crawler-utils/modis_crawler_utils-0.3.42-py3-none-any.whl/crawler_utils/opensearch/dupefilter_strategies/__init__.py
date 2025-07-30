import logging
from typing import Optional

from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured

from crawler_utils.misc import create_instance_from_settings

logger = logging.getLogger(__name__)


class OpenSearchDupeFilterStrategy:
    dupefilter = None

    def before_query_filter(self, request: Request) -> Optional[bool]:
        """
        Filter request before making ES query.
        Returns True if duplicate, False if not, None to query in ES.
        """
        return None

    def query(self, request: Request) -> Optional[dict]:
        """
        Returns ES query to search for request.
        It will be joined with other queries with bool:must.
        """
        return None


class NoOpStrategy(OpenSearchDupeFilterStrategy):
    def before_query_filter(self, request: Request) -> Optional[bool]:
        return False


BASE_DUPEFILTER_STRATEGIES = {
    "noop": f"{__name__}.NoOpStrategy",
    "depth": f"{__name__}.depth_based.DepthBasedStrategy",
    "news": f"{__name__}.depth_based.DefaultNewsStrategy",
    "delta_fetch_items": f"{__name__}.delta_fetch_items.DeltaFetchItemsStrategy",
    "drop_unproductive_requests": f"{__name__}.drop_unproductive_requests.DropUnproductiveRequestsStrategy",
}


class DupeFilterStrategyLoader:
    """
    Loads strategy from DUPEFILTER_STRATEGY setting and ensures single instance of it.
    Setting supports path to strategy class or known alias (see BASE_DUPEFILTER_STRATEGIES).
    Loads NoOpStrategy by default.
    """

    instance = None
    error = None

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        if cls.instance is not None:
            return cls.instance
        if cls.error:
            raise cls.error
        try:
            cls.instance = create_instance_from_settings(
                crawler=crawler,
                settings=crawler.settings,
                setting_key="DUPEFILTER_STRATEGY",
                aliases=BASE_DUPEFILTER_STRATEGIES,
                defaults=[NoOpStrategy],
            )
            logger.info(
                f"Initialized dupefilter strategy {type(cls.instance).__name__}"
            )
            return cls.instance
        except Exception as error:
            cls.error = error
            raise cls.error


class DupeFilterStrategyMiddlewareHook:
    """
    Allows to insert dupefilter strategy in middleware lists without explicitly specifying its type.
    For example, setting
    SPIDER_MIDDLEWARES = {
      'crawler_utils.opensearch.dupefilter_strategies.DupeFilterStrategyMiddlewareHook': 1,
      ...
    }
    will load strategy designated by DUPEFILTER_STRATEGY setting and insert it as first spider middleware.

    Installing such hook in stand/project level settings allows to specify df strategy per spider/job.
    """

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        try:
            return DupeFilterStrategyLoader.from_crawler(crawler)
        except Exception:
            raise NotConfigured()
