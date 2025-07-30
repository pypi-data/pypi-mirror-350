import logging
from json import dumps

from itemadapter import ItemAdapter
from kafka import KafkaProducer


class KafkaPipeline(object):

    def __init__(self, kafka_address, kafka_key, resource_tag_key, default_resource_tag,
                 default_data_type, data_type_key, compression_type):
        self.producer = None
        self.kafka_address = kafka_address
        self.kafka_key = kafka_key
        self.resource_tag_key = resource_tag_key
        self.default_resource_tag = default_resource_tag
        self.data_type_key = data_type_key
        self.default_data_type = default_data_type
        self.compression_type = compression_type
        self.logger = logging.getLogger(KafkaPipeline.__name__)

    @classmethod
    def from_crawler(cls, crawler):
        # Calm down kafka logs
        logging.getLogger("kafka.conn").setLevel(logging.ERROR)
        return cls(
            kafka_address=crawler.settings.get('KAFKA_ADDRESS'),
            kafka_key=crawler.settings.get('KAFKA_KEY'),
            resource_tag_key=crawler.settings.get('KAFKA_RESOURCE_TAG_KEY', 'platform'),
            default_resource_tag=crawler.settings.get('KAFKA_DEFAULT_RESOURCE_TAG', 'crawler'),
            data_type_key=crawler.settings.get('KAFKA_DATA_TYPE_KEY', 'type'),
            default_data_type=crawler.settings.get('KAFKA_DEFAULT_DATA_TYPE', 'data'),
            compression_type=crawler.settings.get('KAFKA_COMPRESSION_TYPE')
        )

    def open_spider(self, spider):
        if hasattr(spider, 'sitemap_name'):
            self.default_resource_tag = spider.sitemap_name
        self.producer = KafkaProducer(bootstrap_servers=self.kafka_address,
                                      value_serializer=lambda x: x.encode('utf-8'),
                                      key_serializer=lambda x: x.encode('utf-8') if x else None,
                                      compression_type=self.compression_type)

    def close_spider(self, spider):
        self.producer.close()

    def process_item(self, item, spider):
        self.export_data(ItemAdapter(item).asdict())
        return item

    def export_data(self, data):
        resource_tag = data.get(self.resource_tag_key, self.default_resource_tag)
        data_type = data.get(self.data_type_key, self.default_data_type)
        topic = str(resource_tag) + '.' + str(data_type)
        try:
            if self.kafka_key in data:
                self.producer.send(topic, value=dumps(data), key=data[self.kafka_key])
            else:
                self.producer.send(topic, value=dumps(data))
        except Exception as e:
            self.logger.error(e, exc_info=True)
