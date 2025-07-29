from . import Session, Request


def get(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
        timeout=None, allow_redirects=True, proxies=None, hooks=None,
        stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("GET", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def options(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
            timeout=None, allow_redirects=True, proxies=None, hooks=None,
            stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("OPTIONS", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def head(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
         timeout=None, allow_redirects=True, proxies=None, hooks=None,
         stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("HEAD", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def post(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
         timeout=None, allow_redirects=True, proxies=None, hooks=None,
         stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("POST", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def put(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
        timeout=None, allow_redirects=True, proxies=None, hooks=None,
        stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("PUT", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def patch(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
          timeout=None, allow_redirects=True, proxies=None, hooks=None,
          stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("PATCH", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def delete(url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
           timeout=None, allow_redirects=True, proxies=None, hooks=None,
           stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request("DELETE", url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)


def make_request(method, url, params=None, *, data=None, headers=None, cookies=None, files=None, auth=None,
                 timeout=None, allow_redirects=True, proxies=None, hooks=None,
                 stream=None, verify=None, cert=None, json=None) -> Request:
    return Session.make_request(method, url, params,
                                data=data, headers=headers, cookies=cookies, files=files, auth=auth,
                                timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks,
                                stream=stream, verify=verify, cert=cert, json=json)
