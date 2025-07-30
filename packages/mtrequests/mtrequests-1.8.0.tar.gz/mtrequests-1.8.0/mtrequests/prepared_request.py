from requests import PreparedRequest

import mtrequests


class PreparedRequest(PreparedRequest):
    def __init__(self):
        super().__init__()
        self.session: "mtrequests.Session" | None = None
        self.request: "mtrequests.Request" | None = None

    def prepare(
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
            session=None,
            request=None
    ):
        self.session = session
        self.request = request
        return super().prepare(
            method=method,
            url=url,
            headers=headers,
            files=files,
            data=data,
            params=params,
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            json=json
        )


__all__ = ("PreparedRequest",)
