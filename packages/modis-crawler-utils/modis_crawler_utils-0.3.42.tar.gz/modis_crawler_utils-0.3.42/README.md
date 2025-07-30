# crawler-utils

Scrapy utils for Modis crawlers projects.

## MongoDB

Some utils connected with mongodb. 

MongoDBPipeline - pipeline for saving items in mongodb. 

Params:
* MONGODB_SERVER - address of mongodb database.
* MONGODB_PORT - port of mongodb database.
* MONGODB_DB - database where to save data.
* MONGODB_USERNAME - username for authentication in MONGODB_DB database.
* MONGODB_PWD - password for authentication.
* DEFAULT_MONGODB_COLLECTION - default collection where to save data (default value is `test`).
* MONGODB_COLLECTION_KEY - key of item which identifies items collection name (`MONGO_COLLECTION`)
 where to save item (default value is `collection`).
* MONGODB_UNIQUE_KEY - key of item which identifies item

## Kafka

Some utils connected with kafka. 

KafkaPipeline - pipeline for pushing items into kafka.

Pipeline outputs data into stream with name `{RESOURCE_TAG}.{DATA_TYPE}`.
Where `RESOURCE_TAG` is tag of resource from which data is crawled and `DATA_TYPE` is type of 
data crawled: `data`, `post`, `comment`, `like`, `user`, `friend`, `share`, `member`, `news`, 
`community`.

 Params:
* KAFKA_ADDRESS - address of kafka broker.
* KAFKA_KEY - key of item which is put into kafka record key.
* KAFKA_RESOURCE_TAG_KEY - key of item which identifies item `RESOURCE_TAG` (default value is `platform`)
* KAFKA_DEFAULT_RESOURCE_TAG - default `RESOURCE_TAG` for crawled items without `KAFKA_RESOURCE_TAG_KEY` (default value is `crawler`)
* KAFKA_DATA_TYPE_KEY - key of item from which identifies item `DATA_TYPE` (default value is `type`).
* KAFKA_DEFAULT_DATA_TYPE - default `DATA_TYPE` for crawled items without `KAFKA_DATA_TYPE_KEY` (default value is `data`).
* KAFKA_COMPRESSION_TYPE - type of data compression in kafka for example `gzip`.

## OpenSearch

OpenSearchRequestsDownloaderMiddleware transforms request-response pair into an item,
and then sends it to the OpenSearch.

Settings:
```
`OPENSEARCH_REQUESTS_SETTINGS` - dict specifying OpenSearch client connections:
    "hosts": Optional[str | list[str]] = "localhost:9200" - hosts with opensearch endpoint,
    "timeout": Optional[int] = 60 - timeout of connections,
    "http_auth": Optional[tuple[str, str]] = None - HTTP authentication if needed,
    "port": Optional[int] = 443 - access port if not specified in hosts,
    "use_ssl": Optional[bool] = True - usage of SSL,
    "verify_certs": Optional[bool] = False - verifying certificates,
    "ssl_show_warn": Optional[bool] = False - show SSL warnings,
    "ca_certs": Optional[str] = None - CA certificate path,
    "client_key": Optional[str] = None - client key path,
    "client_cert": Optional[str] = None - client certificate path,
    "buffer_length": Optional[int] = 500 - number of items in OpenSearchStorage's buffer.

`OPENSEARCH_REQUESTS_INDEX`: Optional[str] = "scrapy-job-requests" - index in OpenSearch.
```

See an example in examples/opensearch.

## CaptchaDetection

Captcha detection middleware for scrapy crawlers.
It gets the HTML code from the response (if present), sends it to the captcha detection web-server
and logs the result.

If you don't want to check exact response if it has captcha, provide meta-key `dont_check_captcha`
with `True` value.

The middleware must be set up with higher precedence (lower number) than RetryMiddleware:
```python
DOWNLOADER_MIDDLEWARES = {
    "crawler_utils.CaptchaDetectionDownloaderMiddleware": 549,  # By default, RetryMiddleware has 550
}
```

Middleware settings:
* ENABLE_CAPTCHA_DETECTOR: bool = True. Whether to enable captcha detection.
* CAPTCHA_SERVICE_URL: str. For an example: http://127.0.0.1:8000

## Sentry logging

You may want to log exceptions during crawling to your Sentry.
Use the `crawler_utils.sentry_logging.SentryLoggingExtension` for this.
Note that sentry_sdk wants to be loaded as earlier as possible.
To satisfy this condition make the extension with negative order:
```python
EXTENSIONS = {
    # Load SentryLogging extension before other extensions.
    "crawler_utils.sentry_logging.SentryLoggingExtension": -1,
}
```

Settings:

SENTRY_DSN: str - Sentry's DSN, where to send events.\
SENTRY_SAMPLE_RATE: float = 1.0 - sample rate for error events. Must be in range from 0.0 to 1.0.\
SENTRY_TRACES_SAMPLE_RATE: float = 1.0 - the percentage chance a given transaction will be sent to Sentry.\
SENTRY_ATTACH_STACKTRACE: bool = False - whether to attach stacktrace for error events.\
SENTRY_MAX_BREADCRUMBS: int = 10 - max breadcrumbs to capture with Sentry.

For an example, check `examples/sentry_logging`.
