from typing import Sequence, Callable

from requests import PreparedRequest
from requests.auth import AuthBase


class RequestHook(AuthBase):
    def __init__(self, auth: AuthBase | None = None,
                 hooks: Sequence[Callable[[PreparedRequest], PreparedRequest]] | None = None):
        self.auth = auth
        if hooks is None:
            hooks = []
        self.hooks = hooks

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        if self.auth:
            r = self.auth(r)
        for hook in self.hooks:
            r = hook(r)
        return r
