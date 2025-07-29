from threading import Lock

from requests.auth import AuthBase

from . import Session, Request, PendingRequest
from .request_hook import RequestHook


class PendingPool:
    def __init__(self, sessions_count=1, keep_cookies=False):
        self.sessions_count = sessions_count
        self.sessions = [Session() for _ in range(sessions_count)]
        self.locks = [Lock() for _ in range(sessions_count)]
        self.active_session = 0
        self.keep_cookies = keep_cookies
        self.alive = True

    def wrap(self, request: Request,
             request_hook: RequestHook | AuthBase | None = None) -> "PendingRequest":
        session = self.sessions[self.active_session]
        lock = self.locks[self.active_session]
        self.active_session = (self.active_session + 1) % self.sessions_count
        request.auth = request_hook
        return PendingRequest(session, request, lock, self.keep_cookies, self)
