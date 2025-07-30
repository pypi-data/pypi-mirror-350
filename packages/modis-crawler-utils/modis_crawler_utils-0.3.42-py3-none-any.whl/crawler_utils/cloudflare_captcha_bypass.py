from urllib.parse import urlparse

import cloudscraper
from scrapy.exceptions import NotConfigured
from scrapy.http import Headers


class CloudflareBypassMiddleware:

    def __init__(self, use_captcha_bypass):
        if not use_captcha_bypass:
            raise NotConfigured()
        self.host_cookies = {}

    @classmethod
    def from_crawler(cls, crawler):
        use_captcha_bypass = crawler.settings.getbool('USE_CF_CAPTCHA_BYPASS', False)
        return cls(use_captcha_bypass)

    def process_request(self, request, spider):
        request_host = urlparse(request.url).hostname
        if request_host not in self.host_cookies.keys():
            clscraper = cloudscraper.create_scraper()
            # TODO: Make support proxy. This request is making without proxy.
            page = clscraper.get(request.url)
            self.host_cookies[f"{request_host}"] = {
                "headers": Headers(clscraper.headers.items()),
                "cookies": dict(page.cookies.items())
            }
            clscraper.close()
        request.headers.update(self.host_cookies[request_host]["headers"])
        request.cookies.update(self.host_cookies[request_host]["cookies"])
