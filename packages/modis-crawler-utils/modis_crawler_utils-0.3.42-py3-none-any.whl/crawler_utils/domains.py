import tldextract
from itemadapter import ItemAdapter


def get_domain(url):
    return tldextract.extract(url).registered_domain


class ItemDomainsCollectorPipeline:

    def __init__(self, crawler):
        self.domains = set()
        crawler.stats.set_value('item_domains', self.domains)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        if url := ItemAdapter(item).get('_url'):
            self.domains.add(get_domain(url))
        return item
