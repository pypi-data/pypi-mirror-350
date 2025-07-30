import logging
from collections import defaultdict
from datetime import datetime
from typing import Optional

from scrapy import Request
from twisted.internet.defer import Deferred, DeferredList

from crawler_utils.opensearch.dupefilter_strategies.delta_fetch_items import (
    DeltaFetchItemsStrategy,
    FingerprintSet,
)
from crawler_utils.opensearch.storage import OpenSearchStorage
from crawler_utils.talisman_job_env import TalismanJobEnvironment

HexFingerprint = str
logger = logging.getLogger(__name__)


def add_effect(deferred: Deferred, callback, *args, **kwargs):
    """
    Add callback to deferred without altering its result
    """

    def _callback(result):
        callback(result, *args, **kwargs)
        return result

    deferred.addCallback(_callback)


class DropUnproductiveRequestsStrategy(DeltaFetchItemsStrategy):
    def __init__(
        self,
        os_storage: OpenSearchStorage,
        index: str,
        job_env: TalismanJobEnvironment = None,
        requests_update_batch_size: int = 100,
    ):
        super().__init__(
            os_storage=os_storage,
            index=index,
            job_env=job_env,
            requests_update_batch_size=requests_update_batch_size,
        )

        self._leads_to_items: dict[HexFingerprint, Deferred[bool]] = defaultdict(Deferred)
        self._depths: dict[HexFingerprint, int] = {}

        self._unproductive_requests = FingerprintSet()
        self._job_start_time = datetime.now().isoformat()

    def query(self, request: Request) -> Optional[dict]:
        return {
            "bool": {
                "should": [
                    {"match": {"unproductive": True}},
                    {"match": {"has_items": True}},
                ],
                "minimum_should_match": 1,
            }
        }

    def process_spider_output(self, response, result, spider):
        parent_request = response.request  # TODO splash/pptr
        parent_fp = self.request_fingerprint(parent_request)
        parent_leads_to_items_dfd = (
            parent_request.meta.get("_leads_to_items")
            or self._leads_to_items[parent_fp]
        )
        add_effect(
            parent_leads_to_items_dfd,
            self._request_status_updated,
            parent_request,
            parent_fp,
        )

        child_status_dfds = []
        yields_items = False
        for entry in result:
            if isinstance(entry, Request):
                child_request = entry
                if child_request.dont_filter:
                    child_status_dfds.append(
                        child_request.meta.setdefault("_leads_to_items", Deferred())
                    )
                else:
                    child_fp = self.request_fingerprint(child_request)
                    child_depth = child_request.meta.get("depth") or (
                        1 + parent_request.meta.get("depth", 0)
                    )
                    if child_depth <= self._depths.setdefault(child_fp, child_depth):
                        child_status_dfds.append(self._leads_to_items[child_fp])
            elif entry is not None:
                yields_items = True

            yield entry

        if not parent_leads_to_items_dfd.called:
            if yields_items:
                parent_leads_to_items_dfd.callback(True)
            elif not child_status_dfds:
                parent_leads_to_items_dfd.callback(False)
            else:
                for child_leads_to_items_dfd in child_status_dfds:
                    add_effect(
                        child_leads_to_items_dfd,
                        self._child_request_status_updated,
                        parent_leads_to_items_dfd,
                    )
                add_effect(
                    DeferredList(child_status_dfds),
                    self._all_child_requests_statuses_updated,
                    parent_leads_to_items_dfd,
                )

    @staticmethod
    def _child_request_status_updated(leads_to_items, parent_leads_to_items_dfd):
        if not parent_leads_to_items_dfd.called and leads_to_items:
            parent_leads_to_items_dfd.callback(True)

    @staticmethod
    def _all_child_requests_statuses_updated(statuses, parent_leads_to_items_dfd):
        if not parent_leads_to_items_dfd.called:
            if all(ok and not leads_to_items for ok, leads_to_items in statuses):
                parent_leads_to_items_dfd.callback(False)

    def _request_status_updated(self, leads_to_items, request, request_fp):
        logger.info(f"Status updated for request {request}: {leads_to_items=}")
        if leads_to_items:
            return
        if not self._unproductive_requests.add(request_fp):
            return
        if self._unproductive_requests.batch_length() < self.requests_update_batch_size:
            return
        self._update_unproductive_requests()

    def _update_unproductive_requests(self):
        self._mark_requests_in_base(
            self._unproductive_requests.pop_batch(), mark="unproductive"
        )

    def close_spider(self, spider):
        self._update_unproductive_requests()
        super().close_spider(spider)
