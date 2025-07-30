# -*- coding: utf-8 -*-
import logging
from urllib.parse import urljoin

import requests
import scrapy
from scrapy.pipelines.files import FilesPipeline as FilesPipelineBase
from scrapy.pipelines.images import ImagesPipeline as ImagesPipelineBase
from scrapy.utils.misc import md5sum

from .files import FilesPipeline

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

logger = logging.getLogger(__name__)


class ImagesPipeline(FilesPipeline):
    """ Pipeline for downloading images.

    This is FilesPipeline configured to work ONLY with images, just like ImagesPipeline from Scrapy.
    FilesPipeline settings are available with 'IMAGES_' prefix instead of 'FILES_', except for image-related
    settings (FILES_PROCESS_IMAGES, FILES_IMAGE_ATTACHMENT_TYPES), which are disabled.
    """

    SAVE_EXTENSION = '.jpg'

    ALLOW_ATTACHMENT_TYPES = ('image',)
    DENY_ATTACHMENT_TYPES = ()

    DEFAULT_IMAGES_RESULT_FIELD = '_attachments'

    DEFAULT_TYPE_TAG = 'image'

    KEY_PREFIX = 'IMAGES'
    CRAWLER_ATTRIBUTE_NAME = 'images_pipeline'

    @classmethod
    def from_settings(cls, settings):
        logger.warning(
            f'{ImagesPipeline.__module__}.{ImagesPipeline.__name__} is deprecated and might be removed in future. '
            f'Consider using {FilesPipeline.__module__}.{FilesPipeline.__name__} instead.')
        return super(FilesPipeline, cls).from_settings(settings)

    def file_downloaded(self, response, request, info, *, item=None):
        return self.image_downloaded(response, request, info, item=item)


class VkImagesPipeline(ImagesPipelineBase):

    def get_media_requests(self, item, info):
        for attachment in item['attachments']:
            if attachment['type'] == 'image':
                yield scrapy.Request(attachment['url'],
                                     meta={'owner_id': item.get('owner_id'),
                                           'photo_id': attachment.get('id')
                                           })

    def file_path(self, request, response=None, info=None):
        owner_id, photo_id = request.meta['owner_id'], request.meta['photo_id']
        return 'vk/%s/%s.jpg' % (owner_id, photo_id)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        owner_id, photo_id = request.meta['owner_id'], request.meta['photo_id']
        return 'vk/%s/thumbs/%s/%s.jpg' % (owner_id, photo_id, thumb_id)

    def item_completed(self, results, item, info):
        super(FilesPipelineBase, self).item_completed(results, item, info)
        for attachment, result in zip(item['attachments'], results):
            ok, value = result
            if ok:
                attachment['url'] = value['path']
                attachment['source'] = value['url']
                attachment['checksum'] = value['checksum']
            else:
                attachment['source'] = attachment['url']
                attachment['url'] = value
            self.spiderinfo.spider.crawler.stats.inc_value('photos_crawled')
        return item


class ImgPushStore(object):

    def __init__(self, store_uri):
        self.store_uri = store_uri

    def persist_file(self, content):
        imgstore_response = requests.post(self.store_uri, files={'file': content})
        if imgstore_response.status_code == 200:
            filename = imgstore_response.json().get('filename')
            return urljoin(self.store_uri, filename)
        return None

    def stat_file(self, path, info):
        return {}


class ImgPushImagesPipeline(FilesPipelineBase):

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)

    @classmethod
    def from_settings(cls, settings):
        store_uri = settings['IMAGE_STORE_URL']
        return cls(store_uri)

    def get_media_requests(self, item, info):
        for attachment in item['attachments']:
            if attachment['type'] == 'image':
                yield scrapy.Request(attachment['url'])

    def _get_store(self, uri):
        return ImgPushStore(uri)

    def file_downloaded(self, response, request, info):
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        return checksum

    def file_path(self, request, response=None, info=None):
        filename = None
        if response:
            filename = self.store.persist_file(response.body)
        return filename

    def item_completed(self, results, item, info):
        super(FilesPipelineBase, self).item_completed(results, item, info)
        for attachment, result in zip(item['attachments'], results):
            ok, value = result
            if ok:
                attachment['url'] = value['path']
                attachment['source'] = value['url']
                attachment['checksum'] = value['checksum']
            else:
                attachment['source'] = attachment['url']
                attachment['url'] = value

        return item
