from typing import List
from urllib.parse import urljoin

import requests
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

from crawler_utils.credentials.credential import Credential
from crawler_utils.credentials.store import CredentialVersionConflictError, CredentialsStore, CredentialsStoreError, \
    NoSuchCredentialError
from crawler_utils.states import StateKey
from crawler_utils.states.talisman_states_api import TalismanStatesAPI, TalismanStatesAPIError
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class TalismanCredentialsStore(CredentialsStore):
    GET_FORMAT = '/api/credentials?domain={domain}&projectId={project_id}'
    GET_BY_ID_FORMAT = '/api/credentials/{id}'

    def __init__(self, api_base_url: str, job_env: TalismanJobEnvironment):
        if api_base_url is None:
            raise NotConfigured('Undefined Crawlers API URL')
        if job_env.project_id is None:
            raise NotConfigured('Undefined project ID')
        self.api_base_url = api_base_url
        self.job_env = job_env
        self._states_api = TalismanStatesAPI(api_base_url, job_env)

    @classmethod
    def from_settings(cls, settings: Settings):
        api_base_url = settings.get('TALISMAN_CRAWLERS_API_BASE_URL')
        job_env = TalismanJobEnvironment.from_settings(settings)
        return cls(api_base_url, job_env)

    def get(self, domain: str) -> List[Credential]:
        url = urljoin(self.api_base_url,
                      self.GET_FORMAT.format(domain=domain, project_id=self.job_env.project_id))
        response = requests.get(url, headers=self.job_env.job_auth_headers)
        self._check_status(response)
        return [self._as_credential(c) for c in response.json()]

    def get_by_id(self, credential_id: int) -> Credential:
        url = urljoin(self.api_base_url, self.GET_BY_ID_FORMAT.format(id=credential_id))
        response = requests.get(url, headers=self.job_env.job_auth_headers)
        self._check_status(response)
        return self._as_credential(response.json())

    def update(self, credential: Credential) -> int:
        try:
            return self._states_api.push_credential_state(credential.full_state, credential.status).version
        except TalismanStatesAPIError as error:
            self._check_status(error.response)

    def _as_credential(self, json):
        credential_id = json.get('id')
        state_key = StateKey(credential_id=credential_id)
        return Credential(
            credential_id=credential_id,
            domain=json.get('domain'),
            credential_type=json.get('dataType'),
            login=json.get('login'),
            password=json.get('password'),
            token=json.get('token'),
            description=json.get('description'),
            status=json.get('status'),
            state_loader=lambda: self._states_api.pull_credential_state(state_key)
        )

    @staticmethod
    def _check_status(response):
        if response.status_code == 404:
            raise NoSuchCredentialError()
        elif response.status_code == 409:
            raise CredentialVersionConflictError()
        elif response.status_code != 200:
            raise TalismanCredentialsStoreError(response)


class TalismanCredentialsStoreError(CredentialsStoreError):
    def __init__(self, response: requests.Response):
        self.response = response
        message = '[{status}] {text}'.format(status=response.status_code, text=response.text)
        super().__init__(message)
