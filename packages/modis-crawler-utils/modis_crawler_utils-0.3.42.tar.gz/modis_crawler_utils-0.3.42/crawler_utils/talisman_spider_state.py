import dataclasses
import logging
import typing
from copy import deepcopy
from functools import cached_property

from scrapy import signals
from scrapy.exceptions import NotConfigured

from crawler_utils.states import State, StateKey
from crawler_utils.states.talisman_states_api import TalismanStatesAPI
from crawler_utils.talisman_job_env import TalismanJobEnvironment

logger = logging.getLogger(__name__)


class TalismanSpiderState:

    def __init__(self,
                 crawlers_api_base_url: str,
                 job_env: TalismanJobEnvironment):
        self.crawlers_api_base_url = crawlers_api_base_url
        self.job_env = job_env

        self._states_api = TalismanStatesAPI(crawlers_api_base_url, job_env)
        self._state: typing.Optional[State] = None

    @classmethod
    def from_crawler(cls, crawler):
        if not (crawlers_api_base_url := crawler.settings.get('TALISMAN_CRAWLERS_API_BASE_URL')):
            raise NotConfigured('No setting: TALISMAN_CRAWLERS_API_BASE_URL')
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        obj = cls(crawlers_api_base_url, job_env)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(obj.spider_closed, signal=signals.spider_closed)
        return obj

    def spider_opened(self, spider):
        spider_cls = type(spider)
        spider_cls.state = cached_property(self._get_spider_state)
        spider_cls.state.attrname = 'state'
        spider.flush = lambda: self._flush_spider_state(spider)

    def spider_closed(self, spider):
        if hasattr(spider, 'before_state_close'):
            spider.before_state_close()
        self._flush_spider_state(spider)

    def _get_spider_state(self, spider):
        if not self.job_env.crawler_id:
            return {}
        logger.info('Loading spider state from Talisman API')
        state_key = StateKey(crawler_id=self.job_env.crawler_id)
        self._state = self._states_api.pull_state(state_key)
        return deepcopy(self._state.state)

    def _flush_spider_state(self, spider):
        if not self._state or self._state.state == spider.state:
            return
        updated_state = dataclasses.replace(self._state, state=spider.state)
        self._state = self._states_api.push_state(updated_state)
