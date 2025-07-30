import dataclasses
import json
import typing
from copy import deepcopy
from pathlib import Path

from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings

from crawler_utils.states import CredentialState, CredentialStatesStore, ID, State, StateKey, StatesStore, \
    VersionConflict


def dict_to_state(state_dict: dict) -> State:
    key = StateKey(**key_dict) if (key_dict := state_dict.pop('key', None)) else None
    return CredentialState(**state_dict, key=key) if 'cookies' in state_dict else State(**state_dict, key=key)


def state_to_dict(state: State) -> dict:
    return dataclasses.asdict(state)


class _LocalStatesStore(StatesStore, CredentialStatesStore):

    def __init__(self):
        self._states = []
        self._state_id_or_key_to_index = {}

    def _append_states(self, *states: State):
        for state in states:
            if not (state.id or state.key):
                raise ValueError('No id or key in state')
            self._states.append(state)
            state_index = len(self._states) - 1
            if state.id:
                self._state_id_or_key_to_index[state.id] = state_index
            if state.key:
                self._state_id_or_key_to_index[state.key] = state_index

    @staticmethod
    def _as_credential_state(state: State) -> CredentialState:
        if isinstance(state, CredentialState):
            return state
        return CredentialState(id=state.id, key=state.key, state=state.state, version=state.version)

    def pull_state(self, id_or_key: typing.Union[ID, StateKey]) -> State:
        if (state_index := self._state_id_or_key_to_index.get(id_or_key)) is not None:
            return deepcopy(self._states[state_index])
        return State(key=id_or_key) if isinstance(id_or_key, StateKey) else State(id=id_or_key)

    def push_state(self, state: State) -> State:
        if not (id_or_key := state.id or state.key):
            raise ValueError('No id or key in state')
        if (state_index := self._state_id_or_key_to_index.get(id_or_key)) is not None:
            existing_state = self._states[state_index]
            if state.version != existing_state.version:
                raise VersionConflict()
            state.version += 1
            self._states[state_index] = deepcopy(state)
        else:
            self._append_states(deepcopy(state))
        return state

    def pull_credential_state(self, id_or_key: typing.Union[ID, StateKey]) -> CredentialState:
        return self._as_credential_state(self.pull_state(id_or_key))

    def push_credential_state(self, state: CredentialState, status: str = 'Valid') -> CredentialState:
        return self._as_credential_state(self.push_state(state))


class InMemoryStatesStore(_LocalStatesStore):

    def __init__(self, states: typing.List[State]):
        super().__init__()
        self._append_states(*deepcopy(states))

    @classmethod
    def from_settings(cls, settings: Settings):
        if not (states := settings.get('STATES')):
            raise NotConfigured('STATES setting is not defined')
        if isinstance(states, str):
            states = json.loads(states)
        states = [state if isinstance(state, State) else dict_to_state(state) for state in states]
        return cls(states)


class FileStatesStore(_LocalStatesStore):

    def __init__(self, states_path: Path):
        super().__init__()
        self.states_path = states_path

    @classmethod
    def from_settings(cls, settings: Settings):
        if not (states_path := settings.get('STATES_PATH')):
            raise NotConfigured('STATES_PATH setting is not defined')
        return cls(Path(states_path))

    def _load_states(self):
        self._states = []
        self._state_id_or_key_to_index = {}
        with open(self.states_path) as states_file:
            states = list(map(dict_to_state, json.load(states_file)))
            self._append_states(*states)

    def _dump_states(self):
        with open(self.states_path, 'w') as states_file:
            state_dicts = list(map(state_to_dict, self._states))
            return json.dump(state_dicts, states_file, indent=2, ensure_ascii=False)

    def pull_state(self, id_or_key: typing.Union[ID, StateKey]) -> State:
        self._load_states()
        return super().pull_state(id_or_key)

    def push_state(self, state: State) -> State:
        self._load_states()
        new_state = super().push_state(state)
        self._dump_states()
        return new_state
