import logging
from urllib.parse import urljoin

import requests
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from crawler_utils.talisman_job_env import TalismanJobEnvironment
from crawler_utils.timestamp import ensure_seconds


class TalismanControllerPipeline:

    def __init__(self,
                 tc_address,
                 tc_id_key,
                 tc_snippet_key,
                 tc_snippet_postfix,
                 tc_topic,
                 resource_tag_key,
                 default_resource_tag,
                 data_type_key,
                 default_data_type,
                 message_priority,
                 job_env,
                 use_talisman_controller_pipeline):
        self.tc_address = tc_address
        self.tc_id_key = tc_id_key
        self.tc_snippet_key = tc_snippet_key
        self.tc_snippet_postfix = tc_snippet_postfix
        self.tc_topic = tc_topic
        self.resource_tag_key = resource_tag_key
        self.default_resource_tag = default_resource_tag
        self.data_type_key = data_type_key
        self.default_data_type = default_data_type
        self.message_priority = message_priority
        self.job_env = job_env
        self.tc_endpoint = urljoin(tc_address, 'messages/add')
        self.logger = logging.getLogger(TalismanControllerPipeline.__name__)
        self.use_talisman_controller_pipeline = use_talisman_controller_pipeline

    @classmethod
    def from_crawler(cls, crawler):
        job_env = TalismanJobEnvironment.from_settings(crawler.settings)
        return cls(
            tc_address=crawler.settings.get('TCONTROLLER_ADDRESS', 'http://tcontroller:8080/'),
            tc_id_key=crawler.settings.get('TCONTROLLER_ID_KEY', '_uuid'),
            tc_snippet_key=crawler.settings.get('TCONTROLLER_SNIPPET_KEY', 'is_snippet'),
            tc_snippet_postfix=crawler.settings.get('TCONTROLLER_SNIPPET_POSTFIX', 'snippet'),
            tc_topic=crawler.settings.get('TCONTROLLER_TOPIC'),
            resource_tag_key=crawler.settings.get('TCONTROLLER_RESOURCE_TAG_KEY', 'platform'),
            default_resource_tag=crawler.settings.get('TCONTROLLER_DEFAULT_RESOURCE_TAG', 'crawler'),
            data_type_key=crawler.settings.get('TCONTROLLER_DATA_TYPE_KEY', 'type'),
            default_data_type=crawler.settings.get('TCONTROLLER_DEFAULT_DATA_TYPE', 'data'),
            message_priority=crawler.settings.get('TCONTROLLER_MESSAGE_PRIORITY'),
            job_env=job_env,
            use_talisman_controller_pipeline=crawler.settings.getbool('TALISMAN_CONTROLLER_PIPELINE_ENABLED', True)
        )

    def open_spider(self, spider):
        if hasattr(spider, 'sitemap_name'):
            self.default_resource_tag = spider.sitemap_name

    def process_item(self, item, spider):
        if self.use_talisman_controller_pipeline:
            self.export_message(ItemAdapter(item).asdict())
            return item
        else:
            raise DropItem("Ignoring item")

    def export_message(self, message):
        message_id = message.get(self.tc_id_key)
        if self.tc_topic:
            topic = self.tc_topic
        else:
            resource_tag = message.get(self.resource_tag_key, self.default_resource_tag)
            data_type = message.get(self.data_type_key, self.default_data_type)
            topic = f'{resource_tag}.{data_type}'
            if message.get(self.tc_snippet_key, False):
                topic = f'{topic}.{self.tc_snippet_postfix}'
        payload = {
            'id': message_id,
            'topic': topic.lower(),
        }
        if self.job_env.job_id:
            payload['jobId'] = self.job_env.job_id
            message["_job_id"] = self.job_env.job_id
        if self.job_env.periodic_job_id:
            payload['periodicJobId'] = self.job_env.periodic_job_id
            message["_periodic_job_id"] = self.job_env.periodic_job_id
        if self.job_env.project_id:
            payload['projectId'] = self.job_env.project_id
            message["_project_id"] = self.job_env.project_id
        if self.job_env.crawler_id:
            payload['crawlerId'] = self.job_env.crawler_id
            message["_crawler_id"] = self.job_env.crawler_id
        if self.job_env.external_search_loader_id:
            message["_external_search_loader_id"] = self.job_env.external_search_loader_id
        if self.job_env.research_map_id:
            message['_research_map_id'] = self.job_env.research_map_id
        payload['message'] = message
        if self.message_priority:
            payload['priority'] = self.message_priority
        timestamp = message.get('_timestamp')
        if timestamp:
            payload['timestamp'] = ensure_seconds(timestamp)
        try:
            response = requests.post(self.tc_endpoint, json=payload)
            if response.status_code == 200:
                self.logger.info(f'Exported message {message_id}')
            else:
                self.logger.error(f'Failed to export message {message_id}: {response.text}')
        except Exception as e:
            self.logger.error(e, exc_info=True)
