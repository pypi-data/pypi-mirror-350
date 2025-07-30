import hashlib
import json
import warnings
from typing import (
    Callable,
    Iterable,
    Optional,
    Union,
)

from scrapy import Request
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.request import fingerprint
from scrapy_splash.dupefilter import splash_request_fingerprint
from scrapypuppeteer import PuppeteerRequest

_INCLUDE_HEADERS_TYPING = Optional[Iterable[Union[bytes, str]]]


def puppeteer_request_fingerprint(
    request: Request,
    *,
    include_headers: _INCLUDE_HEADERS_TYPING = None,
    fallback: Optional[Callable[[Request, _INCLUDE_HEADERS_TYPING], bytes]] = None,
) -> bytes:
    """
    Fingerprint for Puppeteer requests based on Puppeteer action.

    :param request: puppeteer request to be fingerprinted.
    :param include_headers: whether to include headers or not.
    :param fallback: function to be executed on not puppeter- or puppeteer-containing- request.

    :returns: fingerprint as bytes
    """
    warnings.warn(
        "`puppeteer_request_fingerprint` is deprecated and will be moved to scrapy-puppeteer-client library.",
        ScrapyDeprecationWarning,
        stacklevel=2,
    )

    if isinstance(request, PuppeteerRequest):
        fp = fingerprint(request, include_headers=include_headers).hex()
        fp = json.dumps(
            [fp, request.action.endpoint, request.action.payload()], sort_keys=True
        )
        return hashlib.sha1(fp.encode()).digest()

    if puppeteer_request := request.meta.get("puppeteer_request"):
        # Contrary to scrapy-splash, PuppeteerMiddleware produces requests with dont_filter=True,
        # so we have to reuse initial request fingerprint to filter them in subsequent crawls.
        return puppeteer_request_fingerprint(
            puppeteer_request, include_headers=include_headers, fallback=fallback
        )

    return (fallback or fingerprint)(request, include_headers=include_headers)


def _fixed_splash_request_fingerprint(
    request: Request, include_headers: _INCLUDE_HEADERS_TYPING = None
) -> bytes:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return bytes.fromhex(splash_request_fingerprint(
            request, include_headers=include_headers
        ))


def default_request_fingerprint(request: Request) -> bytes:
    """
    Default request fingerprinter for opensearch.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return puppeteer_request_fingerprint(
            request, fallback=_fixed_splash_request_fingerprint
        )
