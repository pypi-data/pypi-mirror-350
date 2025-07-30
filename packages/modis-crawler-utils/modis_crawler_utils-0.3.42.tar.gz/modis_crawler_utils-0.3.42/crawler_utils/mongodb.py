import logging

from bson import BSON
from gridfs import GridFS
from itemadapter import ItemAdapter
from pymongo import MongoClient, DESCENDING
from pymongo.errors import DuplicateKeyError, DocumentTooLarge


class MongoConnection:
    def __init__(self, uri, port, db_name, user, pwd, use_grid_fs, grid_fs_collection):
        self.uri = uri
        self.port = port
        self.db_name = db_name
        self.user = user
        self.pwd = pwd
        self.connection = None
        self.db = None
        self.use_grid_fs = use_grid_fs
        self.grid_fs_collection = grid_fs_collection

    @classmethod
    def from_settings(cls, settings):
        return cls(
            uri=settings.get('MONGODB_SERVER'),
            port=settings.getint('MONGODB_PORT', MongoClient.PORT),
            db_name=settings.get('MONGODB_DB'),
            user=settings.get('MONGODB_USERNAME'),
            pwd=settings.get('MONGODB_PWD'),
            use_grid_fs=settings.getbool('MONGODB_USE_GRID_FS', False),
            grid_fs_collection=settings.get('MONGODB_GRID_FS_COLLECTION', 'fs')
        )

    def open(self):
        self.connection = MongoClient(self.uri, self.port)
        self.db = self.connection[self.db_name]
        if self.user is not None:
            self.db.authenticate(self.user, self.pwd)

    def close(self):
        self.connection.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MongoDBStorage(object):

    def __init__(self, connection):
        self.connection = connection
        self.connection.open()
        self.logger = logging.getLogger(MongoDBStorage.__name__)
        self.grid_fs = GridFS(self.connection.db, collection=connection.grid_fs_collection)

    @classmethod
    def from_crawler(cls, crawler):
        connection = MongoConnection.from_settings(crawler.settings)
        return cls(connection)

    def close(self):
        self.connection.close()

    def create_unique_index(self, field, collection):
        self.connection.db[collection].create_index(field, unique=True)

    def create_descending_index(self, field, collection):
        self.connection.db[collection].create_index([(field, DESCENDING)])

    def save(self, data, collection, unique_key):
        try:
            self.connection.db[collection].insert_one(data)
            self.logger.debug('Saved data (%s)', data)
        except DuplicateKeyError:
            if unique_key in data:
                self.logger.info("Item (%s) already in base.", data[unique_key])
            else:
                self.logger.info("Item (%s) already in base.", data)
        except DocumentTooLarge:
            if self.connection.use_grid_fs:
                try:
                    with self.grid_fs.new_file() as grid_file:
                        grid_file.write(BSON.encode(data))
                        item = {
                            'file_id': grid_file._id,
                        }
                        if unique_key in data:
                            item[unique_key] = data[unique_key]
                        self.connection.db[collection].insert_one(item)

                    self.logger.debug('Saved data by GridFS Bucket (%s)', data)
                except Exception:
                    self.logger.debug("Error with gridFS saving item (%s)", data)
            else:
                self.logger.debug("Document (%s) too large and gridFS off", data)


class MongoDBPipeline(object):

    def __init__(self, storage, default_mongo_collection, mongo_collection_key, mongo_unique_key):
        self.storage = storage
        self.mongo_collection = default_mongo_collection
        self.mongo_collection_key = mongo_collection_key
        self.mongo_unique_key = mongo_unique_key
        if mongo_unique_key:
            self.storage.create_unique_index(mongo_unique_key, self.mongo_collection)

    @classmethod
    def from_crawler(cls, crawler):
        storage = MongoDBStorage.from_crawler(crawler)
        default_mongo_collection = crawler.settings.get('DEFAULT_MONGODB_COLLECTION', "test")
        mongo_collection_key = crawler.settings.get('MONGODB_COLLECTION_KEY', "collection")
        mongo_unique_key = crawler.settings.get('MONGODB_UNIQUE_KEY')
        return cls(storage, default_mongo_collection, mongo_collection_key, mongo_unique_key)

    def open_spider(self, spider):
        if hasattr(spider, 'sitemap_name'):
            self.mongo_collection = spider.sitemap_name

    def close_spider(self, spider):
        self.storage.close()

    def process_item(self, item, spider):
        dict_item = ItemAdapter(item).asdict()
        collection = dict_item.get(self.mongo_collection_key, self.mongo_collection)
        self.storage.save(dict_item, collection, self.mongo_unique_key)
        return item
