from __future__ import annotations

from contextlib import nullcontext
from typing import TYPE_CHECKING
import requests

import mtrequests

if TYPE_CHECKING:
    from . import PendingPool, PendingRequest, PendingResponse, RequestHook


class Request(requests.Request):
    def __init__(
            self,
            method=None,
            url=None,
            headers=None,
            files=None,
            data=None,
            params=None,
            auth=None,
            cookies=None,
            hooks=None,
            json=None,
            send_kwargs=None,
            proxies=None,
            stream=None,
            verify=None,
            cert=None,
    ):
        # Default empty dicts for dict params.
        data = [] if data is None else data
        files = [] if files is None else files
        headers = {} if headers is None else headers
        params = {} if params is None else params
        hooks = {} if hooks is None else hooks

        self.hooks = requests.sessions.default_hooks()
        for k, v in list(hooks.items()):
            self.register_hook(event=k, hook=v)

        self.method = method
        self.url = url
        self.headers = headers
        self.files = files
        self.data = data
        self.json = json
        self.params = params
        self.auth = auth
        self.cookies = cookies

        self.session_arg_send_kwargs = send_kwargs
        self.session_arg_proxies = proxies
        self.session_arg_stream = stream
        self.session_arg_verify = verify
        self.session_arg_cert = cert

    def send(self, repeats=0, delay=0.1, session: "mtrequests.Session" = None, keep_cookies: bool = True) -> PendingResponse | None:
        if session is None:
            session = mtrequests.Session()
            keep_cookies = False
        return mtrequests.PendingRequest(session, self, nullcontext(), keep_cookies, None).send(repeats, delay)  # noqa

    def wrap(self, pending_pool: PendingPool, request_hook: RequestHook = None) -> PendingRequest | None:
        return pending_pool.wrap(self, request_hook)
