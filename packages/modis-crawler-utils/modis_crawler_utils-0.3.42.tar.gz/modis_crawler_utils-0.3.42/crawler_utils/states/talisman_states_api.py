import json
import typing
from urllib.parse import urljoin

import requests
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

from crawler_utils.states import CredentialState, CredentialStatesStore, ID, State, StateKey, StatesStore, \
    VersionConflict
from crawler_utils.talisman_job_env import TalismanJobEnvironment


class TalismanStatesAPIError(Exception):
    def __init__(self, response: requests.Response, *args):
        super().__init__(*args)
        self.response = response


class AccessIsDenied(TalismanStatesAPIError):
    def __init__(self, response: requests.Response):
        super().__init__(response, '403 You have not permission to perform this action')


class EntityNotFound(TalismanStatesAPIError):
    def __init__(self, response: requests.Response):
        super().__init__(response, '404 Entities with such ids do not exist')


class TalismanStatesAPI(StatesStore, CredentialStatesStore):

    def __init__(self, api_base_url: str, job_env: TalismanJobEnvironment):
        self.api_base_url = api_base_url
        self.job_env = job_env

    @classmethod
    def from_settings(cls, settings: Settings) -> 'TalismanStatesAPI':
        if not (api_base_url := settings.get('TALISMAN_CRAWLERS_API_BASE_URL')):
            raise NotConfigured('No setting: TALISMAN_CRAWLERS_API_BASE_URL')
        job_env = TalismanJobEnvironment.from_settings(settings)
        return TalismanStatesAPI(api_base_url, job_env)

    # -------------------------------------------------------------------------
    #
    # States store interfaces
    #

    def pull_state(self, id_or_key: typing.Union[ID, StateKey]) -> State:
        if isinstance(id_or_key, StateKey):
            state = self.get_by_key(id_or_key) or State()
            state.key = id_or_key
            return state
        return self.get_by_id(id_or_key) or State(id=id_or_key)

    def push_state(self, state: State) -> State:
        if state.id:
            new_state = self.update_state(
                state_id=state.id,
                state=state.state,
                version=state.version
            )
        elif state.key:
            new_state = self.add_state(
                state_key=state.key,
                state=state.state
            )
        else:
            raise ValueError('No id or key in state')
        new_state.key = state.key
        return new_state

    def pull_credential_state(self, id_or_key: typing.Union[ID, StateKey]) -> CredentialState:
        if isinstance(id_or_key, StateKey):
            state = self.get_by_key(id_or_key) or CredentialState()
            state.key = id_or_key
        else:
            state = self.get_by_id(id_or_key) or CredentialState(id=id_or_key)
        if not isinstance(state, CredentialState):
            state = CredentialState(
                id=state.id,
                key=state.key,
                state=state.state,
                version=state.version
            )
        return state

    def push_credential_state(self, state: CredentialState, status: str = 'Valid') -> CredentialState:
        if state.id:
            new_state = self.update_state(
                state_id=state.id,
                state=state.state,
                cookies=state.cookies,
                credential_status=status,
                version=state.version
            )
        elif state.key:
            new_state = self.add_state(
                state_key=state.key,
                state=state.state,
                cookies=state.cookies
            )
        else:
            raise ValueError('No id or key in state')
        new_state.key = state.key
        if not isinstance(new_state, CredentialState):
            new_state = CredentialState(
                id=new_state.id,
                key=new_state.key,
                state=new_state.state,
                version=new_state.version
            )
        return new_state

    # -------------------------------------------------------------------------
    #
    # Actual API methods
    #

    def get_by_key(self, state_key: StateKey) -> typing.Optional[State]:
        response = requests.get(url=urljoin(self.api_base_url, '/api/crawl/state'),
                                params=self._to_request_parameters(state_key),
                                headers=self.job_env.job_auth_headers)
        return self._state_from_response(response)

    def get_by_id(self, state_id: ID) -> typing.Optional[State]:
        response = requests.get(url=urljoin(self.api_base_url, f'/api/crawl/state/{state_id}'),
                                headers=self.job_env.job_auth_headers)
        return self._state_from_response(response)

    def add_state(self,
                  state_key: StateKey,
                  state: typing.Dict[str, typing.Any],
                  cookies: typing.Dict[str, str] = None) -> State:
        request_body = {
            'parameters': self._to_request_parameters(state_key),
            'state': json.dumps(state)
        }
        if cookies is not None:
            request_body['cookie'] = json.dumps(cookies)
        response = requests.post(url=urljoin(self.api_base_url, '/api/crawl/state'),
                                 json=request_body,
                                 headers=self.job_env.job_auth_headers)
        return self._state_from_response(response)

    def update_state(self,
                     state_id: ID,
                     version: int,
                     state: typing.Dict[str, typing.Any],
                     cookies: typing.Dict[str, str] = None,
                     credential_status: str = None) -> State:
        request_body = {
            'state': json.dumps(state),
            'stateVersion': version
        }
        if cookies is not None:
            request_body['cookie'] = json.dumps(cookies)
        if credential_status is not None:
            request_body['credentialStatus'] = credential_status
        response = requests.put(url=urljoin(self.api_base_url, f'/api/crawl/state/{state_id}'),
                                json=request_body,
                                headers=self.job_env.job_auth_headers)
        return self._state_from_response(response)

    @staticmethod
    def _to_request_parameters(state_key: StateKey):
        result = {
            'crawlerId': state_key.crawler_id,
            'periodicJobId': state_key.periodic_job_id,
            'credentialId': state_key.credential_id,
            'informationSourceId': state_key.information_source_id,
            'crawlKey': state_key.custom_key
        }
        return {k: str(v) for k, v in result.items() if v}

    @staticmethod
    def _state_from_response(response: requests.Response):
        if response.status_code == 200:
            response_data = response.json()
            state_data = {
                'id': response_data['id'],
                'state': json.loads(response_data['state']),
                'version': response_data['stateVersion']
            }
            if 'cookie' in response_data:
                state_data['cookies'] = json.loads(response_data['cookie'])
                return CredentialState(**state_data)
            return State(**state_data)

        if response.status_code == 204:
            return None

        # TODO do we really need typed errors?
        if response.status_code == 409:
            raise VersionConflict()
        if response.status_code == 403:
            raise AccessIsDenied(response)
        if response.status_code == 404:
            raise EntityNotFound(response)
        raise TalismanStatesAPIError(response, f'Failed to extract state: {response.status_code} {response.text}')
