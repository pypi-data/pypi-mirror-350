# -*- coding: utf-8 -*-
import logging
import json
import datetime

from crawler_utils.talisman_job_env import TalismanJobEnvironment
from logstash import TCPLogstashHandler, LogstashFormatterVersion1
from scrapy import signals
from twisted.internet import task
from requests import post


class ScrapydLogstashFormatter(LogstashFormatterVersion1):

    def __init__(self, job_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_id = job_id

    def get_extra_fields(self, record):
        fields = super(ScrapydLogstashFormatter, self).get_extra_fields(record)

        if self.job_id:
            fields['job_id'] = self.job_id

        return fields


class LogstashLoggerExtension:

    @classmethod
    def from_crawler(cls, crawler):
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        logstash_host = crawler.settings.get("LOGSTASH_LOGGER_HOST", "logstash")
        logstash_port = crawler.settings.getint("LOGSTASH_LOGGER_PORT", 9600)
        root_logger = logging.getLogger()
        logstash_handler = TCPLogstashHandler(logstash_host, logstash_port)
        job_id = job_env.job_id
        logstash_handler.setFormatter(ScrapydLogstashFormatter(job_id))
        logstash_handler.setLevel(crawler.settings.get('LOG_LEVEL', 'INFO'))
        root_logger.addHandler(logstash_handler)
        return cls()


class LogstashDumpStatsExtension(object):
    """
    Enable this extension to log Scrapy stats periodically to Logstash.
    """

    def __init__(self, stats, interval, logstash_uri, job_id):
        self.stats = stats
        self.interval = interval
        self.logstash_uri = logstash_uri
        self.job_id = job_id
        self.task = None

    @classmethod
    def from_crawler(cls, crawler):
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        interval = crawler.settings.getfloat("LOGSTASH_DUMP_STATS_INTERVAL", 60.0)
        logstash_uri = crawler.settings.get("LOGSTASH_DUMP_STATS_URI", "http://logstash:9600")
        job_id = job_env.job_id
        extension = cls(crawler.stats, interval, logstash_uri, job_id)
        crawler.signals.connect(extension.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(extension.spider_closed, signal=signals.spider_closed)
        return extension

    def spider_opened(self, spider):
        self.task = task.LoopingCall(self.push_stats)
        self.task.start(self.interval)

    def spider_closed(self, spider, reason):
        if self.task and self.task.running:
            self.push_stats()
            self.task.stop()

    def push_stats(self):
        stats = self.stats.get_stats()
        if self.job_id:
            stats['job_id'] = self.job_id
        post(self.logstash_uri,
             data=json.dumps(stats, default=self.encode),
             headers={'content-type': 'application/json'})

    @staticmethod
    def encode(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
