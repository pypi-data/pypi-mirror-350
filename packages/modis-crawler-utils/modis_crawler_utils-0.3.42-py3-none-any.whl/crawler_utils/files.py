# -*- coding: utf-8 -*-
import base64
import binascii
import hashlib
import logging
import mimetypes
import re
from collections.abc import Iterable
from contextlib import suppress
from io import BytesIO
from os.path import basename, join, splitext
from typing import BinaryIO, MutableMapping, Optional, Union
from urllib.parse import quote_plus, unquote, urlsplit

from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.pipelines.files import FSFilesStore, FilesPipeline as FilesPipelineBase, GCSFilesStore
from scrapy.pipelines.images import ImageException, ImagesPipeline as ImagesPipelineBase
from scrapy.settings import Settings
from scrapy.utils.defer import deferred_to_future
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import md5sum
from twisted.internet.defer import DeferredList, maybeDeferred

from crawler_utils.opensearch.request_fingerprint import default_request_fingerprint
from crawler_utils.social_media.items import AttachmentType

logger = logging.getLogger(__name__)


def set_attachment_type(attachment: MutableMapping, attachment_type: Optional[str]):
    if attachment_type is None:
        attachment.pop('attachment_type', None)
        attachment.pop('attachment_type_raw', None)
        return
    try:
        attachment['attachment_type'] = AttachmentType(attachment_type).value
        attachment.pop('attachment_type_raw', None)
    except ValueError:
        attachment['attachment_type_raw'] = attachment_type
        attachment.pop('attachment_type', None)


def get_attachment_type(attachment: MutableMapping) -> Optional[str]:
    attachment_type = attachment.get('attachment_type')
    if isinstance(attachment_type, AttachmentType):
        attachment_type = attachment_type.value
    return attachment_type or attachment.get('attachment_type_raw')


class FilesPipeline(ImagesPipelineBase, FilesPipelineBase):
    """ Pipeline for downloading files.

    This pipeline differs from Scrapy's FilesPipeline in several aspects.

    1. Input URL lists may contain attachment-like objects (e.g. social_media.items.Attachment)
    with following attributes

    url: str - URL of file to download; attachments without URLs are ignored
    attachment_type: str - (optional) type of attachment: image, video, etc

    There are two settings controlling which attachment types to download, both are comma separated lists of types

    FILES_ALLOW_ATTACHMENT_TYPES
    Crawl only attachments with these types.
    Default is empty (allow all types).

    FILES_DENY_ATTACHMENT_TYPES
    Crawl all attachments but these types.
    Default is "image". This will change to empty (allow all types) when ImagesPipeline will be removed.

    Attachments without types are always downloaded.

    You may use FILES_ATTACHMENTS_FIELD setting for input field instead of FILES_URLS_FIELD.

    In contrast with default FilesPipeline, successful results are appended to results field in
    items. Default field name to store results is '_attachments'. If input field and results field are same,
    then input attachment objects are updated instead (thus they must support assignment of path, checksum, status
    and filename fields), while bare input URLs are converted to attachment objects.

    2. This pipeline processes attachments not only at the top level, but also in nested items.

    If the input and output fields match, attachments will be updated in-place. Otherwise, for each nested item,
    an output field will be added with the results of collecting attachments extracted from this item.

    The maximum depth of nested items to be processed is determined by the FILES_MAX_NESTED_ITEMS_DEPTH setting.
    By default, attachments are processed at any depth.

    Depth is calculated according to the following rules
    - depth of the original item is 0
    - if the nested element is an item (e.g., dict) and its depth is K, then the depth of values by its keys is K + 1
    - if the nested element is a list (tuple, set) and its depth is K, then the depth of its elements is K + 1

    This means, for example, that for HistoryMessage items in copy_history have depth 2.

    If the same attachments occur at different nesting levels, the files will not be downloaded multiple times,
    but the attachment objects will not be deduplicated.

    3. This pipeline generates paths of format

    <store_uri>/<resource>/<type>/<hash>/.../<hash><sep><filename><ext>

    where

    <store_uri> - store URI from settings; note that this differs from base Scrapy pipelines,
                  where store URI is not included in returned paths
    <resource>  - resource tag (aka platform) from item; it is extracted similar to
                  talisman controller pipeline
    <type>      - attachment type
    <hash>      - one or more segments based on request URL digest
    <sep>       - separator between digest and filename
    <filename>  - actual file name extracted from request or response
    <ext>       - file extension

    This behavior is controlled with a number of settings

    FILES_RESOURCE_TAG_KEY
    Field in item to extract resource tag from. Default is 'platform'.

    FILES_DEFAULT_RESOURCE_TAG
    Provides default value for resource tag if there is no resource tag key in item.
    For sitemaps defaults to sitemap name, otherwise it is 'crawler'.

    FILES_DEFAULT_TYPE_TAG
    Provides default value for attachment type in path. Default is 'data'.

    FILES_DIGEST_ALGORITHM
    Name of algorithm to calculate digest of request URL.
    Any algorithm available in hashlib may be used.
    Default is 'sha1', as in Scrapy's FilesPipeline.

    FILES_DIGEST_ENCODING
    Name of encoding to convert raw digest into path-friendly string.
    Default is 'hex', also supports baseN encodings.

    FILES_DIGEST_PATH_SEGMENT_LENGTHS
    Determines the number and lengths of <hash> segments.
    May be int, iterable of ints, or a string of comma separated ints.
    Lengths are based on encoded digest bytes.
    If empty, digest is not used.
    Default is (4, 4), which by default produces two segments of 4 hex digits.

    FILES_DIGEST_FILENAME_SEPARATOR
    Separates <filename> from <hash> segments.
    May be '/', which results in another hierarchy level.
    Default is '__'.

    FILES_SAVE_EXTENSION
    If provided, files will be saved with this extension. Defaults to None.
    Should start with a dot.

    FILES_MAX_FILENAME_LENGTH
    Limits the length of generated filename component (<hash><sep><filename><ext>).
    Retains extension. Defaults to 100 characters.

    FILES_MAX_PATH_LENGTH
    Limits the length of full generated path. Defaults to None.

    Pipeline attempts to extract original filename from request or response and saves it in results
    under 'filename' key. Options are inspected in the following order:
    - 'filename' key in request meta
    - Content-Disposition header in response
    - last path segment in response URL
    - media type from Content-Type header in response (e.g. image/png -> image.png)
    - last path segment in request URL
    - media type from Content-Type header in request

    4. This pipeline can use image processing capabilities from Scrapy's ImagePipeline. To enable it, one needs to
    enable FILES_PROCESS_IMAGES setting (defaults to False) and list image types in FILES_IMAGE_ATTACHMENT_TYPES
    (defaults to ['image']). Then this pipeline will process compatible attachments as images: convert to JPEG/RGBA,
    filter images based on size with IMAGES_MIN_WIDTH, IMAGES_MIN_HEIGHT settings, generate thumbnails with
    IMAGES_THUMBS setting. Note that there is no FILES_ prefix for these settings; other IMAGES_ settings are ignored.

    Thumbnail paths are generated by modifying attachment types with thumb ids:
    <store_uri>/<resource>/<type>-<thumb id>/<hash>/.../<hash><sep><filename><ext>

    If a file cannot be processed as image, it will be saved as regular file. Paths may differ by extension. Default
    extension for converted images is .jpg. It can be changed with FILES_IMAGE_SAVE_EXTENSION setting, but images
    will still be saved in JPEG format.
    """

    DIGEST_PATH_SEGMENT_LENGTHS = (4, 4)
    DIGEST_ALGORITHM = 'sha1'
    DIGEST_ENCODING = 'hex'
    DIGEST_FILENAME_SEPARATOR = '__'
    SAVE_EXTENSION = None
    MAX_FILENAME_LENGTH = 100
    MAX_PATH_LENGTH = None

    ALLOW_ATTACHMENT_TYPES = ()
    DENY_ATTACHMENT_TYPES = ('image',)

    DEFAULT_FILES_RESULT_FIELD = '_attachments'

    RESOURCE_TAG_KEY = 'platform'
    DEFAULT_RESOURCE_TAG = 'crawler'
    DEFAULT_TYPE_TAG = 'data'

    MAX_NESTED_ITEMS_DEPTH = None

    PROCESS_IMAGES = False
    IMAGE_ATTACHMENT_TYPES = ('image',)
    IMAGE_SAVE_EXTENSION = '.jpg'

    KEY_PREFIX = 'FILES'
    CRAWLER_ATTRIBUTE_NAME = 'files_pipeline'

    crawler: Crawler
    _fingerprinter = None

    def __init__(self, store_uri, download_func=None, settings=None):
        if not store_uri.endswith('/'):
            # Ensure trailing slash for consistency between different stores: in S3/GCS stores
            # prefix and generated path are concatenated, in other stores - joined with slash
            store_uri += '/'

        super().__init__(store_uri, settings=settings, download_func=download_func)

        self._store_uri = store_uri

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        self._digest_path_segment_lengths = self._get_digest_path_segment_lengths(settings)
        if self._digest_path_segment_lengths:
            self._digest_func = self._get_digest_func(settings)
            self._digest_encoder = self._get_digest_encoder(settings)
            self._digest_filename_separator = self._resolve('DIGEST_FILENAME_SEPARATOR', settings)
        self._save_extension = self._resolve('SAVE_EXTENSION', settings)
        self._max_filename_length = self._get_length_constraint('MAX_FILENAME_LENGTH', settings)
        self._max_path_length = self._get_length_constraint('MAX_PATH_LENGTH', settings)

        self._allow_attachment_types = self._get_attachment_types('ALLOW_ATTACHMENT_TYPES', settings)
        self._deny_attachment_types = self._get_attachment_types('DENY_ATTACHMENT_TYPES', settings)

        self._input_field = self._resolve('ATTACHMENTS_FIELD', settings) or self._resolve('URLS_FIELD', settings)
        self._result_field = self._resolve('RESULT_FIELD', settings)
        self._inplace_update = self._input_field == self._result_field

        self._resource_tag_key = self._resolve('RESOURCE_TAG_KEY', settings)
        self._default_resource_tag = self._resolve('DEFAULT_RESOURCE_TAG', settings)
        self._default_type_tag = self._resolve('DEFAULT_TYPE_TAG', settings)

        self._max_nested_items_depth = self._resolve('MAX_NESTED_ITEMS_DEPTH', settings, int)
        if self._max_nested_items_depth is None:
            self._max_nested_items_depth = float('inf')

        self._process_images = self._resolve_bool('PROCESS_IMAGES', settings)
        if self._process_images:
            self._image_attachment_types = self._get_attachment_types('IMAGE_ATTACHMENT_TYPES', settings)
            self._image_save_extension = self._resolve('IMAGE_SAVE_EXTENSION', settings)

        self.expires = self._resolve('EXPIRES', settings, int)

    @classmethod
    def from_settings(cls, settings):
        return super(ImagesPipelineBase, cls).from_settings(settings)

    @classmethod
    def from_crawler(cls, crawler: 'Crawler'):
        # Bind pipeline to crawler object to reuse download caches in spiders
        # TODO maybe it is better to create a singleton metaclass instead?
        if pipeline := getattr(crawler, cls.CRAWLER_ATTRIBUTE_NAME, None):
            return pipeline
        pipeline = super().from_crawler(crawler)
        setattr(crawler, cls.CRAWLER_ATTRIBUTE_NAME, pipeline)
        return pipeline

    def _resolve_key(self, key, settings):
        return self._key_for_pipe(f'{self.KEY_PREFIX}_{key}',
                                  base_class_name='FilesPipeline',
                                  settings=settings)

    def _resolve(self, key, settings, value_type=None):
        resolved_key = self._resolve_key(key, settings)
        if resolved_key in settings:
            value = settings[resolved_key]
        elif hasattr(self, resolved_key):
            value = getattr(self, resolved_key)
        else:
            value = getattr(self, key, None)
        if value_type is not None and value is not None:
            return value_type(value)
        return value

    def _resolve_bool(self, key, settings):
        return settings.getbool(self._resolve_key(key, settings), getattr(self, key, False))

    def _get_digest_path_segment_lengths(self, settings):
        lengths = self._resolve('DIGEST_PATH_SEGMENT_LENGTHS', settings)
        if lengths is None:
            return None
        if isinstance(lengths, str):
            lengths = [int(length.strip()) for length in lengths.split(',')]
        elif isinstance(lengths, Iterable):
            lengths = [int(length) for length in lengths]
        else:
            length = int(lengths)
            lengths = [] if length == 0 else [length]
        if any([length <= 0 for length in lengths]):
            raise ValueError('Digest segment lengths must be positive')
        return lengths

    def _get_digest_func(self, settings):
        algorithm = self._resolve('DIGEST_ALGORITHM', settings)
        if not algorithm:
            raise ValueError('Digest algorithm must not be empty')
        try:
            return getattr(hashlib, algorithm)
        except AttributeError:
            raise ValueError(f'Unknown digest algorithm {algorithm}')

    def _get_digest_encoder(self, settings):
        encoding = self._resolve('DIGEST_ENCODING', settings)
        if not encoding:
            raise ValueError('Digest encoding must not be empty')
        encoding = encoding.lower()
        if encoding == 'hex':
            return binascii.hexlify
        elif encoding == 'base64':
            return base64.urlsafe_b64encode
        elif encoding == 'base32':
            return base64.b32encode
        elif encoding == 'base16':
            return base64.b16encode
        else:
            # TODO consider other encodings
            raise ValueError(f'Unsupported digest encoding {encoding}')

    def _get_length_constraint(self, key, settings):
        length = self._resolve(key, settings, value_type=int)
        if length is None:
            return None
        if length < 0:
            raise ValueError(f'{key} must be non-negative')
        return length

    def _get_attachment_types(self, key, settings):
        types = self._resolve(key, settings)
        if not types:
            return []
        if isinstance(types, str):
            return [t.strip() for t in types.split(',')]
        return list(types)

    # --------------------------------------------------------------------------

    def open_spider(self, spider):
        if not self._fingerprinter and (fingerprinter := getattr(self.crawler, 'request_fingerprinter', None)):
            # (Scrapy>=2.11) None if pipeline is initialized before dupefilter/fingerprinter
            self._fingerprinter = fingerprinter
        super().open_spider(spider)
        if hasattr(spider, 'sitemap_name'):
            self._default_resource_tag = spider.sitemap_name

    def process_item(self, item, spider, item_depth=0):
        tasks = []
        if item_depth < self._max_nested_items_depth:
            for key, value in list(ItemAdapter(item).items()):
                if key not in (self._input_field, self._result_field):
                    tasks.extend(self._process_nested_items(value, spider, item_depth + 1))
        tasks.append(super().process_item(item, spider))
        dfd = DeferredList(tasks, consumeErrors=True)
        return dfd.addCallback(lambda _: item)

    def _process_nested_items(self, nested_item, spider, nested_item_depth):
        if ItemAdapter.is_item(nested_item) and nested_item_depth <= self._max_nested_items_depth:
            yield self.process_item(nested_item, spider, nested_item_depth)
        elif isinstance(nested_item, (list, tuple, set)) and nested_item_depth < self._max_nested_items_depth:
            for element in nested_item:
                yield from self._process_nested_items(element, spider, nested_item_depth + 1)

    def get_media_requests(self, item, info, item_depth=0):
        item_adapter = ItemAdapter(item)
        resource_tag = item_adapter.get(self._resource_tag_key, self._default_resource_tag)
        urls_or_attachments = item_adapter.get(self._input_field, [])
        attachments = [
            {'url': url_or_attachment} if isinstance(url_or_attachment, str) else url_or_attachment
            for url_or_attachment in urls_or_attachments
        ]
        if self._inplace_update:
            urls_or_attachments[:] = attachments

        for attachment in map(ItemAdapter, attachments):
            if self._is_to_be_downloaded(attachment):
                yield Request(
                    attachment['url'],
                    meta={
                        'attachment': attachment,
                        'resource_tag': resource_tag,
                        'is_image_request': (self._process_images
                                             and get_attachment_type(attachment) in self._image_attachment_types)
                    }
                )

    def _process_request(self, request, info, *args, **kwargs):
        def on_result(result):
            result = result.copy()  # don't modify cached results
            result['path'] = join(self._store_uri, result['path'])
            if 'filename' not in result:
                result['filename'] = self._filename(request, None)
            if self._inplace_update:
                attachment = request.meta['attachment']
                for key, value in result.items():
                    with suppress(KeyError):
                        attachment[key] = value
            return result

        def on_failure(failure):
            logger.error(f'Failed to download file {request.url}',
                         exc_info=failure_to_exc_info(failure),
                         extra={'spider': info.spider})
            return failure

        return super()._process_request(request, info, *args, **kwargs).addCallbacks(on_result, on_failure)

    def item_completed(self, results, item, info):
        if not results:
            return item
        if self._inplace_update:
            return item  # results should be already written
        with suppress(KeyError):
            item_adapter = ItemAdapter(item)
            if item_adapter.get(self._result_field) is None:
                item_adapter[self._result_field] = []
            item_adapter[self._result_field].extend(r for ok, r in results if ok)
        return item

    def media_downloaded(self, response, request, info, *, item=None):
        result = super().media_downloaded(response, request, info)
        result['filename'] = self._filename(request, response)
        return result

    def file_downloaded(self, response, request, info, *, item=None):
        if request.meta.get('is_image_request', False):
            try:
                return self.image_downloaded(response, request, info, item=item)
            except ImageException:  # fired when image is too small
                raise
            except Exception:  # TODO narrow down
                logger.warning(f'Failed to process {request.url} as image, saving as regular file',
                               exc_info=True)
        request.meta['is_image_request'] = False
        return FilesPipelineBase.file_downloaded(self, response, request, info, item=item)

    def file_path(self, request, response=None, info=None, *, item=None):
        path = self._file_path(request, response, info)
        return self._truncate_path(path)

    def thumb_path(self, request, thumb_id, response=None, info=None, *, item=None):
        attachment = request.meta.get('attachment') or {'url': request.url}
        type_tag = get_attachment_type(attachment) or self._default_type_tag
        thumb_type_tag = f'{type_tag}-{thumb_id}' if type_tag else thumb_id
        thumb_attachment = {**attachment}
        set_attachment_type(thumb_attachment, thumb_type_tag)
        thumb_request = request.replace(meta={**request.meta, 'attachment': thumb_attachment})
        return self.file_path(thumb_request, response, info)

    # --------------------------------------------------------------------------

    def persist(self,
                data: Union[bytes, BinaryIO],
                store_path: str = None,
                url: str = None,
                filename: str = None,
                resource_tag: str = None,
                type_tag: str = None,
                close_stream: bool = False):
        """
        Persists given data, which may be bytes or binary file object.
        If store_path is given, uses this path, otherwise generates path by given url and optional filename.
        Store path must be relative to store URI.
        Pass close_stream=True to close file after transfer (False by default).
        Returns two objects: optional deferred which resolves when saving is completed,
         and a dict with url, path and checksum.
        """
        if store_path:
            if not filename:
                filename = basename(store_path)
        else:
            if not url:
                raise ValueError('Either url or store_path must be provided')
            if not filename:
                filename = self._filename_from_url(url)
            attachment = {'url': url, 'filename': filename}
            set_attachment_type(attachment, type_tag)
            request = Request(url, meta={'attachment': attachment, 'resource_tag': resource_tag})
            store_path = self.file_path(request, info=self.spiderinfo)

        if isinstance(data, bytes):
            data = BytesIO(data)
            close_stream = True
        elif isinstance(self.store, (FSFilesStore, GCSFilesStore)):
            # these stores support only BytesIO buffer
            data.seek(0)
            data_bytes = data.read()
            if close_stream:
                data.close()
            data = BytesIO(data_bytes)
            close_stream = True

        data.seek(0)
        checksum = md5sum(data)
        data.seek(0)
        dfd = maybeDeferred(self.store.persist_file, store_path, data, info=self.spiderinfo)
        result = {
            'url': url,
            'path': join(self._store_uri, store_path),
            'checksum': checksum,
            'filename': filename
        }
        if close_stream:
            def _close(result_or_failure):
                data.close()
                return result_or_failure

            dfd.addBoth(_close)
        return dfd, result

    async def persist_future(self,
                             data: Union[bytes, BinaryIO],
                             store_path: str = None,
                             url: str = None,
                             filename: str = None,
                             resource_tag: str = None,
                             type_tag: str = None,
                             close_stream: bool = False):
        """
        Persists given data, which may be bytes or binary file object.
        If store_path is given, uses this path, otherwise generates path by given url and optional filename.
        Pass close_stream=True to close file after transfer (False by default).
        When saving is completed, returns dict with url, path and checksum.
        """
        dfd, result = self.persist(data, store_path, url, filename, resource_tag, type_tag, close_stream)
        if dfd:
            await deferred_to_future(dfd)
        return result

    def persist_response(self,
                         response,
                         request=None,
                         resource_tag: str = None,
                         type_tag: str = None,
                         cache: bool = True):
        """
        Persists contents of given response in store using usual path generation scheme.
        Returns two objects: optional deferred which resolves when saving is completed,
         and a dict with url, path and checksum.
        """
        request = request or response.request or Request(response.url)
        path = self.file_path(request, response=response, info=self.spiderinfo)
        filename = self._filename(request, response)
        dfd, result = self.persist(response.body,
                                   url=request.url,
                                   store_path=path,
                                   filename=filename,
                                   resource_tag=resource_tag,
                                   type_tag=type_tag)
        if cache:
            # Cache response in pipeline so it won't be downloaded again
            # TODO Should we await for saving completion? Because Scrapy's FilesPipeline doesn't.
            if self._fingerprinter:
                fp = self._fingerprinter.fingerprint(request)
            else:
                fp = default_request_fingerprint(request)
            self.spiderinfo.downloaded[fp] = {**result, 'status': 'saved manually'}
        return dfd, result

    async def persist_response_future(self,
                                      response,
                                      request=None,
                                      resource_tag: str = None,
                                      type_tag: str = None,
                                      cache: bool = True):
        """
        Persists contents of given response in store using usual path generation scheme.
        When saving is completed, returns dict with url, path and checksum.
        """
        dfd, result = self.persist_response(response, request, resource_tag, type_tag, cache)
        if dfd:
            await deferred_to_future(dfd)
        return result

    # --------------------------------------------------------------------------

    def _is_to_be_downloaded(self, attachment: ItemAdapter):
        if not attachment.get('url'):
            return False
        if not attachment.get('to_be_downloaded', True):
            return False
        if attachment.get('status'):
            return False  # already processed
        attachment_type = get_attachment_type(attachment)
        if not attachment_type:
            return True
        if self._allow_attachment_types:
            return attachment_type in self._allow_attachment_types
        if self._deny_attachment_types:
            return attachment_type not in self._deny_attachment_types
        return True

    def _filename(self, request, response):
        if attachment := request.meta.get('attachment'):
            if (filename := attachment.get('filename')) is not None:
                return filename
        if response:
            return self._filename_from_response(response)
        return self._filename_from_request(request)

    def _filename_from_response(self, response):
        headers = response.headers
        content_disposition = headers.get('Content-Disposition')
        if content_disposition:
            content_disposition = unquote(content_disposition.decode(headers.encoding))
            filename_match = re.search(r'filename=(.+?)(;|$)', content_disposition)
            if filename_match:
                return filename_match.group(1).strip('\"')

        filename = self._filename_from_url(response.url)
        return filename if '.' in filename else filename + self._extension_from_content_type(response.headers)

    def _filename_from_request(self, request):
        filename = self._filename_from_url(request.url)
        return filename if '.' in filename else filename + self._extension_from_content_type(request.headers)

    @staticmethod
    def _filename_from_url(url):
        return unquote(urlsplit(url.rstrip('/')).path.rsplit('/', 1)[-1])

    @staticmethod
    def _extension_from_content_type(headers):
        content_type = headers.get('Content-Type')
        if not content_type:
            return ''
        str_content_type = content_type.decode('utf-8')
        return mimetypes.guess_extension(str_content_type.split(';', 1)[0]) or ''

    def _file_path(self, request, response=None, info=None):
        path = ''
        if resource_tag := request.meta.get('resource_tag') or self._default_resource_tag:
            path += '/' + resource_tag
        if type_tag := get_attachment_type(request.meta.get('attachment', {})) or self._default_type_tag:
            path += '/' + type_tag
        if self._digest_path_segment_lengths:
            digest = self._digest_func(request.url.encode('utf-8')).digest()
            encoded_digest = self._digest_encoder(digest).decode('utf-8')
            for segment_length in self._digest_path_segment_lengths:
                if not encoded_digest:
                    break
                path += '/' + encoded_digest[:segment_length]
                encoded_digest = encoded_digest[segment_length:]
            if self._digest_filename_separator:
                path += self._digest_filename_separator

        path += self._filename(request, response)

        if extension := self._image_save_extension if request.meta.get('is_image_request') else self._save_extension:
            path = splitext(path)[0] + extension

        if not isinstance(self.store, FSFilesStore):
            path = '/'.join(map(quote_plus, path.split('/')))

        return path.lstrip('/')

    def _truncate_path(self, path):
        dirname, filename = path.rsplit('/', 1)
        if self._max_filename_length and len(filename) > self._max_filename_length:
            filename, ext = splitext(filename)
            filename = filename[:self._max_filename_length - len(ext)] + ext
        path = dirname + '/' + filename
        if self._max_path_length and len(path) > self._max_path_length:
            path, ext = splitext(path)
            path = path[:self._max_path_length - len(ext)] + ext
        return path
