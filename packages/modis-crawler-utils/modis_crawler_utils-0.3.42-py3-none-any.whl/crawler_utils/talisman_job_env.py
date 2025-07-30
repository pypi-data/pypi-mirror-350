import dataclasses
import os


@dataclasses.dataclass
class TalismanJobEnvironment:
    job_id: str = None
    project_id: str = None
    crawler_id: str = None
    version_id: str = None
    periodic_job_id: str = None
    research_map_id: str = None
    credential_id: str = None
    job_token: str = None
    external_search_loader_id: str = None

    @classmethod
    def from_settings(cls, settings):
        return cls(
            job_id=settings.get('TALISMAN_CRAWLERS_JOB_ID') or os.environ.get('SCRAPY_JOB'),
            project_id=settings.get('TALISMAN_CRAWLERS_PROJECT_ID'),
            crawler_id=settings.get('TALISMAN_CRAWLERS_SPIDER_ID'),
            version_id=settings.get('TALISMAN_CRAWLERS_VERSION_ID'),
            periodic_job_id=settings.get('TALISMAN_CRAWLERS_PERIODIC_JOB_ID'),
            external_search_loader_id=settings.get('TALISMAN_EXTERNAL_SEARCH_LOADER_ID'),
            research_map_id=settings.get('TALISMAN_CRAWLERS_RESEARCH_MAP_ID'),
            credential_id=settings.get('TALISMAN_CRAWLERS_CREDENTIAL_ID'),
            job_token=settings.get('TALISMAN_CRAWLERS_JOB_TOKEN')
        )

    @property
    def job_auth_headers(self):
        headers = {}
        if self.job_id is not None:
            headers['job_id'] = self.job_id
        if self.job_token is not None:
            headers['X-Auth-Token'] = self.job_token
        return headers
