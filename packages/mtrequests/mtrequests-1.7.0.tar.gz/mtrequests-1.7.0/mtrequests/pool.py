import requests
import threading

from . import Request, Session


class Pool:
    def __init__(self, tasks=None, other_thread_count=0, keep_cookies=False):
        if tasks is None:
            tasks = []
        self.other_thread_count = other_thread_count
        self.keep_cookies = keep_cookies
        self.tasks: list[Request] = tasks
        self.sessions: list[Session] = []
        self.results: list[list[requests.Response | Exception]] = []
        self.threads: list[threading.Thread] = []
        self.is_alive = True

    def make_and_push_request(
            self,
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
    ):
        self.tasks.append(Session.make_request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        ))

    def push(self, request: Request):
        self.tasks.append(request)

    def execute(self):
        self.sessions = [Session() for _ in range(self.other_thread_count + 1)]
        self.results = [[] for _ in range(self.other_thread_count + 1)]
        L = len(self.tasks)
        N = self.other_thread_count + 1
        for i in range(1, N):
            th = threading.Thread(target=self.thread_execute, args=(i, L, N))
            self.threads.append(th)
            th.start()
        self.thread_execute(0, L, N)
        for th in self.threads:
            th.join()
        results = []
        for i in zip(*self.results):
            results.extend(i)
        self.results = results
        return results

    def thread_execute(self, i, L, N):
        session = self.sessions[i]
        for j in range(i, L + 1, N):
            if not self.is_alive:
                break
            try:
                request = self.tasks[j]
                response = session.prepare_and_send(request, self.keep_cookies)
                self.results[i].append(response)
            except IndexError:
                continue
            except Exception as exc:
                self.results[i].append(exc)
