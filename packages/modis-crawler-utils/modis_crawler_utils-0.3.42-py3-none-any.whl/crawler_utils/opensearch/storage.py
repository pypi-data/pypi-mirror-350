# -*- coding: utf-8 -*-
import logging
import typing

import certifi
from opensearchpy import OpenSearch, helpers
from scrapy.crawler import Crawler


class OpenSearchStorage:
    """
    OpenSearchStorage implements high-level access to OpenSearch client.
    """

    DEFAULT_HOSTS = "localhost:9200"
    DEFAULT_BUFFER_LENGTH = 500
    DEFAULT_TIMEOUT = 60
    DEFAULT_PORT = 443
    DEFAULT_USE_SSL = True

    def __init__(self, os: OpenSearch, buffer_length: int):
        self.os = os
        self.buffer_length = buffer_length
        self.items_buffer = []

    @classmethod
    def from_settings(cls, os_settings: dict):
        """
        Initialize OpenSearchStorage from scrapy OpenSearch settings.
        """
        os_settings = os_settings.copy()
        buffer_length = os_settings.pop("buffer_length", cls.DEFAULT_BUFFER_LENGTH)
        os = cls.init_os_client(os_settings)
        return cls(os, buffer_length)

    @classmethod
    def init_os_client(cls, os_settings: dict) -> OpenSearch:
        """
        Initialize OpenSearch client.

        Example os_settings:
            {
                "hosts": "localhost:9200",           # optional
                "timeout": 60,                       # optional
                "http_auth": ("login", "password"),  # optional
                "port": 443,                         # optional
                "use_ssl": True,                     # optional
                "verify_certs": False,               # optional
                "ssl_show_warn": False,              # optional
                "ca_certs": "path_to_ca_certs",      # optional
                "client_key": "path_to_key",         # optional
                "client_cert": "path_to_cert",       # optional
                "buffer_length": 500,                # optional
            }
        """
        os_settings.setdefault("hosts", cls.DEFAULT_HOSTS)
        if not isinstance(os_settings["hosts"], list):
            os_settings["hosts"] = [os_settings["hosts"]]

        if "verify_certs" not in os_settings:
            os_settings["verify_certs"] = False
            os_settings["ssl_show_warn"] = False
        if (
            "client_cert" in os_settings or "client_key" in os_settings
        ) and "ca_certs" not in os_settings:
            os_settings["ca_certs"] = certifi.where()

        os_settings.setdefault("timeout", cls.DEFAULT_TIMEOUT)
        os_settings.setdefault("port", cls.DEFAULT_PORT)
        os_settings.setdefault("use_ssl", cls.DEFAULT_USE_SSL)

        return OpenSearch(**os_settings)

    def search(
        self, body: typing.Optional[dict] = None, index: typing.Optional[str] = None
    ):
        # TODO: more parameters?
        return self.os.search(body=body, index=index)

    def index_exists(self, index):
        return self.os.indices.exists(index)

    def index_item(self, index, item):
        index_action = {
            "_index": index,
            "_source": item,
        }
        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.buffer_length:
            self.send_items()

    def send_items(self, refresh="false"):
        helpers.bulk(self.os, self.items_buffer, refresh=refresh)
        self.items_buffer = []

    def has_pending_items(self):
        return bool(self.items_buffer)

    def refresh_index(self, index):
        self.os.indices.refresh(index)

    def update_by_query(self, index, query, script, **kwargs):
        body = {
            "query": query,
            "script": script,
        }
        return self.os.update_by_query(index, body=body, **kwargs)

    def exists_by_query(self, index, query, **kwargs):
        return self.os.count(index=index, body={"query": query}, **kwargs)["count"] > 0

    def close(self):
        if self.has_pending_items():
            self.send_items()


class OpenSearchStorageLoader:
    instances = {}

    @classmethod
    def from_crawler(cls, crawler: Crawler, os_settings_key: str):
        instance_or_error = cls.instances.get(os_settings_key)
        if instance_or_error is None:
            os_settings = crawler.settings.getdict(os_settings_key)
            try:
                instance_or_error = OpenSearchStorage.from_settings(os_settings)
                cls.instances[os_settings_key] = instance_or_error
                log_level = crawler.settings.get("OPENSEARCH_LOG_LEVEL", logging.ERROR)
                logging.getLogger("opensearch").setLevel(log_level)
                return instance_or_error
            except Exception as error:
                cls.instances[os_settings_key] = error
                raise error
        elif isinstance(instance_or_error, OpenSearchStorage):
            return instance_or_error
        else:
            raise instance_or_error
