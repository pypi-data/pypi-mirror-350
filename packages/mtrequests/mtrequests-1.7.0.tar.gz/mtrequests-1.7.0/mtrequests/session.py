import requests
from requests.cookies import RequestsCookieJar, merge_cookies
from requests.sessions import merge_setting, merge_hooks
from requests.utils import get_netrc_auth, CaseInsensitiveDict
from http import cookiejar as cookielib

from .request import Request
from .prepared_request import PreparedRequest
from .pending_response import PendingResponse


class Session(requests.Session):
    def __init__(self):
        super().__init__()
        self.requests_count = 0

        self._prep: PreparedRequest | None = None
        self._resp: PendingResponse | None = None

    def prepare_and_send(self, request: Request, keep_cookie=False) -> requests.Response:
        self.requests_count += 1
        if keep_cookie is False:
            self.cookies = requests.sessions.cookiejar_from_dict({})
        prep = self.prepare_request(request)
        self._prep = prep

        proxies = request.session_arg_proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, request.session_arg_stream,
            request.session_arg_verify, request.session_arg_cert
        )

        send_kwargs = request.session_arg_send_kwargs
        send_kwargs.update(settings)
        resp = self.send(prep, **send_kwargs)
        self._resp = resp

        return resp

    def prepare_request(self, request):
        cookies = request.cookies or {}

        if not isinstance(cookies, cookielib.CookieJar):
            cookies = requests.sessions.cookiejar_from_dict(cookies)

        # Merge with session cookies
        merged_cookies = merge_cookies(
            merge_cookies(RequestsCookieJar(), self.cookies), cookies
        )

        # Set environment's basic authentication if not explicitly set.
        auth = request.auth
        if self.trust_env and not auth and not self.auth:
            auth = get_netrc_auth(request.url)

        p = PreparedRequest()
        p.prepare(
            method=request.method.upper(),
            url=request.url,
            files=request.files,
            data=request.data,
            json=request.json,
            headers=merge_setting(
                request.headers, self.headers, dict_class=CaseInsensitiveDict
            ),
            params=merge_setting(request.params, self.params),
            auth=merge_setting(auth, self.auth),
            cookies=merged_cookies,
            hooks=merge_hooks(request.hooks, self.hooks),
            session=self,
            request=request
        )
        return p


    @staticmethod
    def make_request(
            method,
            url,
            params=None,
            data=None,
            headers=None,
            cookies=None,
            files=None,
            auth=None,
            timeout=None,
            allow_redirects=True,
            proxies=None,
            hooks=None,
            stream=None,
            verify=None,
            cert=None,
            json=None,
    ) -> Request:
        send_kwargs = {
            "timeout": timeout,
            "allow_redirects": allow_redirects,
        }
        return Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            send_kwargs=send_kwargs,
            proxies=proxies,
            stream=stream,
            verify=verify,
            cert=cert,
        )

    @property
    def prep(self):
        return self._prep
