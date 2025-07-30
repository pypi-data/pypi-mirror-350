import json
import logging
from urllib.parse import urljoin, urlparse

import requests
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, Request, Response

logger = logging.getLogger(__name__)


def uri_validator(url):
    # TODO:
    # very bad, because https://docs.python.org/3/library/urllib.parse.html
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


class CaptchaDetectionDownloaderMiddleware:
    """
        Captcha detection middleware for scrapy crawlers.
    It gets the HTML code from the response (if present), sends it to the captcha detection web-server
    and logs the result.

        If you don't want to check exact response if it has captcha, provide meta-key `dont_check_captcha`
    with `True` value.

        Middleware settings:
        * ENABLE_CAPTCHA_DETECTOR: bool = True. Whether to enable captcha detection.
        * CAPTCHA_SERVICE_URL: str. For an example: http://127.0.0.1:8000
    """

    CAPTCHA_SERVICE_URL_SETTING = "CAPTCHA_SERVICE_URL"
    ENABLE_CAPTCHA_DETECTOR_SETTING = "ENABLE_CAPTCHA_DETECTOR"

    def __init__(self, captcha_service_url: str):
        global logger

        self.captcha_detection_endpoint = urljoin(
            captcha_service_url, "captcha_detector"
        )
        self.logger = logger

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        if not crawler.settings.getbool(cls.ENABLE_CAPTCHA_DETECTOR_SETTING, False):
            raise NotConfigured()

        captcha_service_url = crawler.settings.get(cls.CAPTCHA_SERVICE_URL_SETTING)
        if captcha_service_url is None:
            raise ValueError("Captcha service URL setting is missing.")
        elif not isinstance(captcha_service_url, str):
            raise TypeError(
                f"{cls.CAPTCHA_SERVICE_URL_SETTING} must be a string, got {type(captcha_service_url)}"
            )
        else:
            if not uri_validator(captcha_service_url):
                raise RuntimeError(f"{captcha_service_url} is not a valid URL.")
        return cls(captcha_service_url)

    @staticmethod
    def process_request(request, spider):
        return None

    def process_response(self, request: Request, response: Response, spider):
        if not isinstance(response, HtmlResponse):
            return response

        # Corresponding request could be lost due to other middlewares
        request_to_check = response.request or request
        if request_to_check.meta.get("dont_check_captcha", False):
            return response

        captcha_server_response = requests.post(
            self.captcha_detection_endpoint,
            data=json.dumps({"html_page": response.text}),
        )

        if captcha_server_response.status_code != 200:
            self.logger.warning(
                f"The page {request_to_check} could not be processed by captcha-server"
            )
        else:
            has_captcha = bool(json.loads(captcha_server_response.text)["has_captcha"])
            self.logger.info(
                f"The page {request_to_check} {'has' if has_captcha else 'does not have'} captcha on the page.",
            )
        return response
