import logging

from scrapy.utils.log import TopLevelFormatter, _get_handler, configure_logging


# Код взят из https://stackoverflow.com/questions/35641360/multiple-spiders-in-crawlerprocess-how-to-get-a-log-per-spider
class MyTopLevelFormatter(TopLevelFormatter):
    def __init__(self, loggers, name):
        super().__init__()
        self.loggers = loggers or []
        self.name = name

    def filter(self, record):
        if self.name in record.name:
            return False
        try:
            if record.spider.name != self.name:
                return False  # type:ignore
            record.name = record.spider.name + "." + record.name  # type:ignore
        except AttributeError:
            pass
        try:
            if record.crawler.spidercls.name != self.name:
                return False  # type:ignore
            record.name = record.crawler.spidercls.name + "." + record.name  # type:ignore
        except AttributeError:
            pass
        if any(record.name.startswith(l + ".") for l in self.loggers):
            record.name = record.name.split(".", 1)[0]
        return True


def log_init(settings, name):
    configure_logging(settings, install_root_handler=False)
    handler = _get_handler(settings)
    handler.addFilter(MyTopLevelFormatter(loggers=[__name__], name=name))
    logging.root.addHandler(handler)
