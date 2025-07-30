import time

from scrapy import signals
from twisted.internet import task


def _histogram(values, bins_count):  # could use numpy for that
    counts = [0] * bins_count
    if not values:
        return counts
    min_value, max_value = min(values), max(values)
    bin_size = (max_value - min_value) / bins_count
    if not bin_size:
        counts[bins_count // 2] = len(values)
        return counts
    for value in values:
        bin_index = int((value - min_value) / bin_size)
        counts[min(bin_index, bins_count - 1)] += 1
    return counts


class RequestTimerExtension:
    """
    Records request durations in seconds and reports (min, mid, max) histogram to stats.

    TODO think of more granular timing for puppeteer requests
    """

    TIMER_ID_META_KEY = '_request_timer_id'

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.total_requests_count = 0
        self.active_requests_start_times = {}  # id to start time
        self.finished_requests_durations = []
        crawler.signals.connect(self.request_reached_downloader, signal=signals.request_reached_downloader)
        crawler.signals.connect(self.request_left_downloader, signal=signals.request_left_downloader)

        update_stats_interval = crawler.settings.getint('REQUEST_TIMER_UPDATE_STATS_INTERVAL_SECONDS', 60)
        task.LoopingCall(self.update_stats).start(update_stats_interval, now=False)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def request_reached_downloader(self, request, spider):
        self.total_requests_count += 1
        timer_id = self.total_requests_count  # assume sequential access
        request.meta[self.TIMER_ID_META_KEY] = timer_id
        self.active_requests_start_times[timer_id] = time.time()

    def request_left_downloader(self, request, spider):
        if timer_id := request.meta.pop(self.TIMER_ID_META_KEY, None):
            if start_time := self.active_requests_start_times.pop(timer_id, None):
                self.finished_requests_durations.append(time.time() - start_time)
                self.update_stats()

    def update_stats(self):
        if not self.total_requests_count:
            return
        current_time = time.time()
        active_durations = [current_time - start_time for start_time in self.active_requests_start_times.values()]
        all_durations = self.finished_requests_durations + active_durations
        [min_count, mid_count, max_count] = _histogram(all_durations, bins_count=3)
        self.stats.set_value('request_time_frequency/min_time', min_count / self.total_requests_count)
        self.stats.set_value('request_time_frequency/mid_time', mid_count / self.total_requests_count)
        self.stats.set_value('request_time_frequency/max_time', max_count / self.total_requests_count)
