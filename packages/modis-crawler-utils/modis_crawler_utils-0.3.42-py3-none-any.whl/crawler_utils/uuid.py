import uuid
from itemadapter import ItemAdapter


class UUIDPipeline(object):

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        if "_uuid" not in item_dict:
            item_dict["_uuid"] = str(uuid.uuid4())
        return item_dict

