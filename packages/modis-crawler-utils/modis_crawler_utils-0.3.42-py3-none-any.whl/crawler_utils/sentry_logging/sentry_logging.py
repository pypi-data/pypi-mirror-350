import sentry_sdk
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured


class SentryLoggingExtension:
    """
    A Scrapy extension to catch all exceptions and send them to Sentry.

    Settings:

    SENTRY_DSN: str - Sentry's DSN, where to send events.
    SENTRY_SAMPLE_RATE: float = 1.0 - sample rate for error events. Must be in range from 0.0 to 1.0.
    SENTRY_TRACES_SAMPLE_RATE: float = 1.0 - the percentage chance a given transaction will be sent to Sentry.
    SENTRY_ATTACH_STACKTRACE: bool = False - whether to attach stacktrace for error events.
    """

    def __init__(
        self,
        sentry_dsn: str,
        sentry_sample_rate: float,
        sentry_traces_sample_rate,
        sentry_attach_stacktrace: bool,
        sentry_max_breadcrumbs: int,
        spider_name: str,
    ):
        sentry_sdk.init(
            dsn=sentry_dsn,
            sample_rate=sentry_sample_rate,
            traces_sample_rate=sentry_traces_sample_rate,
            attach_stacktrace=sentry_attach_stacktrace,
            max_breadcrumbs=sentry_max_breadcrumbs,
        )

        sentry_sdk.set_tag("spider_name", spider_name)

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        settings = crawler.settings

        sentry_dsn = settings.get("SENTRY_DSN", None)
        if sentry_dsn is None:
            raise NotConfigured()

        sentry_sample_rate = settings.get("SENTRY_SAMPLE_RATE", 1.0)
        sentry_traces_sample_rate = settings.get("SENTRY_TRACES_SAMPLE_RATE", 1.0)
        sentry_attach_stacktrace = settings.get("SENTRY_ATTACH_STACKTRACE", False)
        sentry_max_breadcrumbs = settings.get("SENTRY_MAX_BREADCRUMBS", 10)

        return cls(
            sentry_dsn,
            sentry_sample_rate,
            sentry_traces_sample_rate,
            sentry_attach_stacktrace,
            sentry_max_breadcrumbs,
            spider_name=crawler.spider.name,
        )
