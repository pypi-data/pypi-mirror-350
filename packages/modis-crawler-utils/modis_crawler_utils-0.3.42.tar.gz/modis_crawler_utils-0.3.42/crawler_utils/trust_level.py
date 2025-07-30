from itemadapter import ItemAdapter


class TrustLevelPipeline(object):

    def __init__(self, trust_level):
        self.trust_level = trust_level

    @classmethod
    def from_crawler(cls, crawler):
        trust_level = crawler.settings.getfloat('TRUST_LEVEL') if 'TRUST_LEVEL' in crawler.settings else None
        return cls(trust_level)

    def process_item(self, item, spider):
        if "_trust_level" not in item and self.trust_level is not None:
            item_dict = ItemAdapter(item).asdict()
            item_dict["_trust_level"] = self.trust_level
            return item_dict
        else:
            return item
