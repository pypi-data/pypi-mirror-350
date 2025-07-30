import abc
import dataclasses
import typing

from scrapy.exceptions import NotConfigured

from crawler_utils.misc import create_instance_from_settings

ID = typing.Union[str, int]


@dataclasses.dataclass(frozen=True)
class StateKey:
    crawler_id: ID = None
    periodic_job_id: ID = None
    information_source_id: ID = None
    credential_id: ID = None
    custom_key: str = None


@dataclasses.dataclass
class State:
    id: ID = None
    key: StateKey = None
    state: dict = dataclasses.field(default_factory=lambda: {})
    version: int = 0


@dataclasses.dataclass
class CredentialState(State):
    cookies: typing.Dict[str, str] = dataclasses.field(default_factory=lambda: {})


class StatesStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pull_state(self, id_or_key: typing.Union[ID, StateKey]) -> State:
        pass

    @abc.abstractmethod
    def push_state(self, state: State) -> State:
        pass


class CredentialStatesStore(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pull_credential_state(self, id_or_key: typing.Union[ID, StateKey]) -> CredentialState:
        pass

    @abc.abstractmethod
    def push_credential_state(self, state: CredentialState, status: str = 'Valid') -> CredentialState:
        pass


class VersionConflict(Exception):
    def __init__(self):
        super().__init__('The specified version of the state does not match current')


_BUILTIN_STORES = {
    'talisman': f'{__name__}.talisman_states_api.TalismanStatesAPI',
    'memory': f'{__name__}.local_store.InMemoryStatesStore',
    'file': f'{__name__}.local_store.FileStatesStore'
}


def create_states_store(settings):
    if store := create_instance_from_settings(
            crawler=None,
            settings=settings,
            setting_key='STATES_STORE',
            aliases=_BUILTIN_STORES,
            defaults=_BUILTIN_STORES.values()):
        return store
    raise NotConfigured('Failed to load states store')
