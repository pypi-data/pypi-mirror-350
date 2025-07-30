import abc
import json
from copy import deepcopy
from pathlib import Path
from typing import List

from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

from crawler_utils.credentials.credential import Credential
from crawler_utils.credentials.store import CredentialVersionConflictError, CredentialsStore, NoSuchCredentialError
from crawler_utils.states import CredentialState


def dict_to_credential(credential_dict: dict) -> Credential:
    full_state = CredentialState(
        state=credential_dict.pop('state', {}),
        cookies=credential_dict.pop('cookies', {}),
        version=credential_dict.pop('version', 0)
    )
    return Credential(**credential_dict, full_state=full_state)


def credential_to_dict(credential: Credential) -> dict:
    credential_dict = {
        'credential_id': credential.id,
        'domain': credential.domain,
        'credential_type': credential.type,
        'login': credential.login,
        'password': credential.password,
        'token': credential.token,
        'description': credential.description,
        'status': credential.status,
        'state': credential.state,
        'cookies': credential.cookies,
        'version': credential.version
    }
    return {k: v for k, v in credential_dict.items() if v is not None}


class _LocalCredentialsStore(CredentialsStore, metaclass=abc.ABCMeta):

    def _index_credentials(self, credentials: List[Credential]):
        self._credentials = {credential.id: credential for credential in credentials}

    def get(self, domain: str) -> List[Credential]:
        return [deepcopy(credential) for credential in self._credentials.values() if credential.domain == domain]

    def get_by_id(self, credential_id: int) -> Credential:
        if credential := self._credentials.get(credential_id):
            return deepcopy(credential)
        raise NoSuchCredentialError()

    def update(self, credential: Credential) -> int:
        if not (stored_credential := self._credentials.get(credential.id)):
            raise NoSuchCredentialError()
        if credential.version != stored_credential.version:
            raise CredentialVersionConflictError()
        stored_credential = deepcopy(credential)
        stored_credential.version += 1
        self._credentials[credential.id] = stored_credential
        return stored_credential.version


class InMemoryCredentialsStore(_LocalCredentialsStore):

    def __init__(self, credentials: List[Credential]):
        self._index_credentials(deepcopy(credentials))

    @classmethod
    def from_settings(cls, settings: Settings):
        if not (credentials := settings.get('CREDENTIALS')):
            raise NotConfigured('CREDENTIALS setting is not defined')
        if isinstance(credentials, str):
            credentials = json.loads(credentials)
        credentials = [credential if isinstance(credential, Credential) else dict_to_credential(credential)
                       for credential in credentials]
        return cls(credentials)


class FileCredentialsStore(_LocalCredentialsStore):

    def __init__(self, credentials_path: Path):
        self.credentials_path = credentials_path

    @classmethod
    def from_settings(cls, settings: Settings):
        if not (credentials_path := settings.get('CREDENTIALS_PATH')):
            raise NotConfigured('CREDENTIALS_PATH setting is not defined')
        return cls(Path(credentials_path))

    def _load_credentials(self):
        with open(self.credentials_path) as credentials_file:
            credentials = list(map(dict_to_credential, json.load(credentials_file)))
            self._index_credentials(credentials)

    def _dump_credentials(self):
        with open(self.credentials_path, 'w') as credentials_file:
            credential_dicts = list(map(credential_to_dict, self._credentials.values()))
            return json.dump(credential_dicts, credentials_file, indent=2, ensure_ascii=False)

    def get(self, domain: str) -> List[Credential]:
        self._load_credentials()
        return super().get(domain)

    def get_by_id(self, credential_id: int) -> Credential:
        self._load_credentials()
        return super().get_by_id(credential_id)

    def update(self, credential: Credential) -> int:
        self._load_credentials()
        new_version = super().update(credential)
        self._dump_credentials()
        return new_version
