from typing import Optional

from scrapy import Request
from scrapy.settings import Settings

from crawler_utils.opensearch.dupefilter_strategies import (
    OpenSearchDupeFilterStrategy,
)


class DepthBasedStrategy(OpenSearchDupeFilterStrategy):
    DEFAULT_MIN_REQUEST_DEPTH = 0

    def __init__(self, min_request_depth: int = DEFAULT_MIN_REQUEST_DEPTH):
        self.min_request_depth = min_request_depth

    @classmethod
    def from_settings(cls, settings: Settings):
        return cls(
            settings.getint(
                "DUPEFILTER_MIN_REQUEST_DEPTH", cls.DEFAULT_MIN_REQUEST_DEPTH
            )
        )

    def before_query_filter(self, request: Request) -> Optional[bool]:
        if int(request.meta.get("depth", 0)) < self.min_request_depth:
            return False
        return None


class DefaultNewsStrategy(DepthBasedStrategy):
    DEFAULT_MIN_REQUEST_DEPTH = 2
