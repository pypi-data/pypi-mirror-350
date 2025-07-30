from functools import cached_property
from typing import Callable, Optional

from crawler_utils.states import CredentialState, StateKey


class Credential:
    # TODO convert to dataclass

    def __init__(self,
                 credential_id: int,
                 domain: str,
                 credential_type: str,  # Account or Token
                 login: Optional[str] = None,
                 password: Optional[str] = None,
                 token: Optional[str] = None,
                 description: Optional[str] = None,
                 status: str = 'Valid',  # Valid or Invalid
                 full_state: Optional[CredentialState] = None,
                 state_loader: Optional[Callable[[], CredentialState]] = None):
        self.id = credential_id
        self.domain = domain
        if credential_type == 'Account':
            if login is None or password is None or token is not None:
                raise ValueError('Invalid account value')
        elif credential_type == 'Token':
            if token is None or login is not None or password is not None:
                raise ValueError('Invalid token value')
        else:
            raise ValueError('Credential type must be "Account" or "Token"')
        self.type = credential_type
        self.login = login
        self.password = password
        self.token = token
        self.description = description
        if status not in {'Valid', 'Invalid'}:
            raise ValueError('Credential status must be "Valid" or "Invalid"')
        self.status = status
        self._state_loader = state_loader if callable(state_loader) else lambda: full_state

    def get_login(self):
        if self.type == "Account":
            return self.login
        else:
            raise ValueError("Tried to get login value for token credential")

    def get_password(self):
        if self.type == "Account":
            return self.password
        else:
            raise ValueError("Tried to get password value for token credential")

    def get_token(self):
        if self.type == "Token":
            return self.token
        else:
            raise ValueError("Tried to get token value for account credential")

    @cached_property
    def full_state(self) -> CredentialState:
        return self._state_loader() or CredentialState(key=StateKey(credential_id=self.id))

    def get_state(self) -> dict:
        return self.full_state.state

    def set_state(self, state: dict):
        self.full_state.state = state

    state = property(get_state, set_state)

    def get_cookies(self) -> dict:
        return self.full_state.cookies

    def set_cookies(self, cookies: dict):
        self.full_state.cookies = cookies

    cookies = property(get_cookies, set_cookies)

    def get_version(self) -> int:
        return self.full_state.version

    def set_version(self, version: int):
        self.full_state.version = version

    version = property(get_version, set_version)

    def __repr__(self):
        return f'Credential(id={self.id})'
