import abc
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

import scrapy
from scrapy import signals


@dataclass
class FocusHint:
    group: str  # e.g. args, settings, selectors
    value: str  # name to inspect


class Focusable(scrapy.Spider, abc.ABC):
    """
    Mixin for spiders to indicate focusable configuration
    """

    @abc.abstractmethod
    def check_focused(self) -> Iterable[FocusHint]:
        pass


class SpiderFocusCheckerExtension:
    """
    Outputs configuration parameters that can help optimize spider traversal into metrics
    """

    def __init__(self, crawler):
        self.stats = crawler.stats
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_opened(self, spider):
        if not isinstance(spider, Focusable):
            return

        focus_hints = defaultdict(set)
        for hint in spider.check_focused():
            focus_hints[hint.group].add(hint.value)

        self.stats.set_value('focus_check/needs_focus', bool(focus_hints))
        for group, values in focus_hints.items():
            self.stats.set_value(f'focus_check/list_focus_{group}', values)
