from scrapy import Request
from scrapy.http import HtmlResponse

ECHO_URL = 'about:blank'


class EchoRequest(Request):
    """
    Request which is to be responded with given response or blank EchoResponse.
    Use it together with EchoDownloaderMiddleware to skip unnecessary start requests and proceed to their callbacks.

    Example:

    class MySpider(scrapy.Spider):
        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'crawler_utils.echo.EchoDownloaderMiddleware': 1
            }
        }

        def start_requests(self):
            yield EchoRequest(callback=self.callback_to_execute)

        def callback_to_execute(self, response, **kwargs):
            # do stuff

    """

    def __init__(self, response=None, **kwargs):
        kwargs.setdefault('url', ECHO_URL)
        kwargs.setdefault('dont_filter', True)
        super().__init__(**kwargs)
        self.response = response
        self.meta.setdefault('dont_index', True)

    def __str__(self):
        return f'<ECHO {super().__str__()}>'


class EchoResponse(HtmlResponse):

    def __str__(self):
        return f'<ECHO {super().__str__()}>'


class EchoDownloaderMiddleware:
    """
    Immediately responds to EchoRequests.
    """

    @staticmethod
    def process_request(request, spider):
        if isinstance(request, EchoRequest):
            return request.response or EchoResponse(url=request.url)
