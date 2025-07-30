import abc
from typing import List

from scrapy.exceptions import NotConfigured

from crawler_utils.credentials import Credential
from crawler_utils.misc import create_instance_from_settings


class CredentialsStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get(self, domain: str) -> List[Credential]:
        pass

    @abc.abstractmethod
    def get_by_id(self, credential_id: int) -> Credential:
        pass

    @abc.abstractmethod
    def update(self, credential: Credential) -> int:
        pass


class CredentialsStoreError(Exception):
    pass


class NoSuchCredentialError(CredentialsStoreError):
    pass


class CredentialVersionConflictError(CredentialsStoreError):
    pass


_BUILTIN_STORES = {
    'talisman': f'{__name__}.talisman.TalismanCredentialsStore',
    'memory': f'{__name__}.local.InMemoryCredentialsStore',
    'file': f'{__name__}.local.FileCredentialsStore'
}


def create_credentials_store(settings):
    if store := create_instance_from_settings(
            crawler=None,
            settings=settings,
            setting_key='CREDENTIALS_STORE',
            aliases=_BUILTIN_STORES,
            defaults=_BUILTIN_STORES.values()):
        return store
    raise NotConfigured('Failed to load credentials store')
