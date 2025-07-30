import random
import threading
import time
from queue import Queue
from threading import Thread

from onionrequests.OnionSession import OnionSession
from onionrequests.exceptions.InvalidHTTPMethodException import InvalidHTTPMethodException


class OnionQueue:
    def __init__(self, sessions: list = None, num_threads: int = 3, balance_session_requests: bool = True,
                 wait_time_s_after_request: float or int = 0.25):
        """
        :param sessions: Any default list of OnionSession objects to use.
        :param num_threads:
            The number of threads to use while processing the task queue. Each one requires its own
            OnionSession, so more will be created if too few have been provided.
        :param balance_session_requests:
            If True, the number of requests will be tracked and averaged between all OnionSessions, then
            those with a request count high above average will be slowed. In other words, sessions that are
            handling requests too quickly will be slowed down so that tasks are more evenly distributed.
        """
        if sessions is not None:
            assert isinstance(sessions, list)
            assert len(sessions) == sum([isinstance(x, OnionSession) for x in sessions])
        assert isinstance(num_threads, int)
        assert num_threads >= 1
        assert isinstance(balance_session_requests, bool)
        assert isinstance(wait_time_s_after_request, float) or isinstance(wait_time_s_after_request, int)
        assert wait_time_s_after_request >= 0

        self.__is_running = False
        self.__num_threads = num_threads
        self.__threads = []
        self.__threads_running = {}
        self.__queue = Queue()

        self.sessions = sessions if sessions is not None else []
        assert isinstance(self.sessions, list)
        while len(self.sessions) < self.__num_threads:
            self.sessions.append(OnionSession())
        self.__balance_session_requests = balance_session_requests
        self.__wait_time_s_after_request = wait_time_s_after_request

        self.__balance_error_multiplier = 0.1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __del__(self):
        self.stop()

    def __get_average_num_session_requests(self):
        total = 0
        num_empty_sessions = 0
        for session in self.sessions:
            if hasattr(session, "num_requests"):
                total += session.num_requests
            else:
                total += 0
                num_empty_sessions += 1
        return total / (len(self.sessions) - num_empty_sessions)

    def __should_throttle_session_for_balancing(self, num_session_requests: int) -> bool:
        """
        This method determines if a session is making too many requests and should be halted temporarily.

        If too many requests are made from the same session to the same website, the website may block
        the session based on IP address. Instead of risking that, tasks are distributed to sessions
        somewhat evenly based on the number of requests they have made -- too many above the average
        results in a pause.

        :param num_session_requests: The current number of requests made by the session.
        :return: True if this thread should be throttled, or False if not.
        """
        assert isinstance(num_session_requests, int)
        assert num_session_requests >= 0
        if not self.__balance_session_requests:
            return False

        '''
        * The balance error is multiplied by the number of queue threads and added to the average 
          number of requests for all sessions. This is the maximum number of requests per session
          before it is paused.
        * A balance error of 0 means any session with an above-average number of requests is paused 
          (perfect split of tasks between sessions). A balance error above 0 adds fuzziness to this 
          split (some sessions can accept more tasks than others).
        '''
        error = self.__balance_error_multiplier * self.__num_threads
        max_requests = self.__get_average_num_session_requests() + error
        return num_session_requests > max_requests

    def __threading_target(self, session: OnionSession):
        self.__threads_running[str(threading.current_thread().ident)] = True
        try:
            session.num_requests = 0
            while self.__is_running:  # Only check self.__is_running to see if the loop should be running.
                # Wait for the session to balance itself before checking for a task.
                while self.__is_running and self.__should_throttle_session_for_balancing(session.num_requests):
                    time.sleep(0.1)

                # Wait for an item to be added to the queue.
                while self.__is_running and self.__queue.empty():
                    time.sleep(random.uniform(0.01, 0.1))

                # After all waiting has finished, check again that the threads should be running. Break if not.
                if not self.__is_running:
                    break

                # Process the task, but raise an exception and stop all threads if something goes wrong.
                try:
                    task_data = self.__queue.get()
                except Exception:
                    # If a queue item could not be found, but one previously existed, assume it's a collision
                    # problem between threads and restart the loop for this one.
                    continue

                # Get all variables necessary for the request.
                url = task_data["url"]
                args = task_data["req_args"]
                kwargs = task_data["req_kwargs"]
                res_handler = task_data["res_handler"]
                handler_args = task_data["handler_args"]
                handler_kwargs = task_data["handler_kwargs"]
                method = str(task_data["method"]).upper()

                # Make the request and track the number of requests made.
                # (Raise for status is False so any errors can be handled in the request handler.)
                if method == "GET":
                    res = session.get(url, *args, **kwargs)
                elif method == "HEAD":
                    res = session.head(url, *args, **kwargs)
                elif method == "POST":
                    res = session.post(url, *args, **kwargs)
                elif method == "PUT":
                    res = session.put(url, *args, **kwargs)
                elif method == "DELETE":
                    res = session.delete(url, *args, **kwargs)
                elif method == "OPTIONS":
                    res = session.options(url, *args, **kwargs)
                elif method == "PATCH":
                    res = session.patch(url, *args, **kwargs)
                else:
                    raise InvalidHTTPMethodException(invalid_method=task_data["method"])

                session.num_requests += 1

                # Handle the request in whatever way the user needs.
                res_handler(res, session, *handler_args, **handler_kwargs)

                # Indicate that this task has been completed.
                self.__queue.task_done()
                time.sleep(self.__wait_time_s_after_request)
        except Exception as ex:
            self.__is_running = False
            raise ex
        finally:
            self.__threads_running[str(threading.current_thread().ident)] = False

    def add_task(
            self, url: str, response_handler, method: str = "GET",
            req_args: list = [], req_kwargs: dict = {},
            handler_args: list = [], handler_kwargs: dict = {}
    ) -> None:
        """
        :param url: The URL to query using an OnionSession object.
        :param response_handler: A function to send the response received from "session.get" or "session.post".
        :param method: Can be one of the following: GET, HEAD, POST, PUT, DELETE, OPTIONS, or PATCH. Default is GET.
        :param req_args: A list of arguments to pass to the session's "get" or "post" method.
        :param req_kwargs: A dictionary of keyword arguments to pass to the session's "get" or "post" method.
        :param handler_args: A list of arguments that are forwarded to the request handler with the request.
        :param handler_kwargs: A dictionary of keyword arguments that are forwarded to the request handler
            with the request.

        Note about the args/kwargs arguments:
            "req_args" and "req_kwargs" are used during the request "GET" or "POST". For example, if you
            need to post JSON data to the server, this is how you would forward that to the session's
            "post" method.

            "handler_args" and "handler_kwargs" allow you to pass additional context to your custom
            request handler -- context that cannot easily be retrieved from just a response alone.
            An example could be in the event of downloading a file, where you must provide a save path to
            your request handler to save the request bytes.

            Here's some example code to further describe the differences:
                with session.get(url, *req_args, **req_kwargs) as res:
                    res.raise_for_status()
                    res_handler(res, session, *handler_args, **handler_kwargs)  # Returns None.
        """
        assert isinstance(method, str)
        assert isinstance(req_args, list) or isinstance(req_args, tuple)
        assert isinstance(req_kwargs, dict)
        assert isinstance(handler_args, list) or isinstance(handler_args, tuple)
        assert isinstance(handler_kwargs, dict)

        method = method.upper().strip(' ')
        if method not in ("GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"):
            raise InvalidHTTPMethodException(invalid_method=method)

        task_data = {
            "url": url,
            "res_handler": response_handler,
            "method": method,
            "req_args": req_args,
            "req_kwargs": req_kwargs,
            "handler_args": handler_args,
            "handler_kwargs": handler_kwargs
        }
        self.__queue.put_nowait(task_data)

    def clear_task_queue(self) -> None:
        assert not self.is_running(), "Cannot clear task queue while tasks are running."
        self.stop()
        self.__queue = Queue()

    def is_running(self) -> bool:
        """
        :return: Returns True if the OnionQueue object is currently processing tasks or is waiting for new
                 tasks to be added to an empty queue, or False otherwise.
        """
        if self.__is_running:
            return True
        else:
            keys = tuple(self.__threads_running.keys())
            for key in keys:
                if self.__threads_running[key]:
                    return True
        return False

    def num_tasks_remaining(self) -> int:
        return self.__queue.unfinished_tasks

    def set_balance_error_multiplier(self, new_multiplier: float or int) -> None:
        """
        A balance error of 0 means any session with an above-average number of requests is paused
        (perfect split of tasks between sessions). A balance error above 0 adds fuzziness to this
        split (some sessions can accept more tasks than others).

        Check the OnionQueue.__should_throttle_session_for_balancing(...) method for more info
        on how it's used.

        :param new_multiplier: Any number equal to or greater than 0.
        """
        assert isinstance(new_multiplier, int) or isinstance(new_multiplier, float)
        assert new_multiplier >= 0
        self.__balance_error_multiplier = new_multiplier

    def start(self) -> None:
        self.__is_running = True
        self.__threads_running = {}
        assert len(self.sessions) >= self.__num_threads
        for x in range(self.__num_threads):  # Not for each session because len(sessions) may be > num threads.
            session = self.sessions[x]
            thread = Thread(target=self.__threading_target, args=(session,))
            thread.daemon = True
            self.__threads.append(thread)
            thread.start()

    def stop(self) -> None:
        thread_id_str = str(threading.current_thread().ident)

        # Set the class global bool to False so other threads know to stop, then wait for them to do so.
        self.__is_running = False
        keys = tuple(self.__threads_running.keys())
        for key in keys:
            if key == thread_id_str:
                # False to prevent infinite looping and to tell other threads this one is finished.
                self.__threads_running[key] = False
            while key in self.__threads_running and self.__threads_running[key]:
                time.sleep(0.01)
        self.__threads_running = {}

        # Join the stopped threads.
        for thread in self.__threads:
            assert isinstance(thread, threading.Thread)
            if str(thread.ident) == thread_id_str:
                # Skip this thread because it cannot join itself.
                continue
            thread.join()
        self.__threads = []

    def wait_for_tasks(self) -> None:
        while self.num_tasks_remaining() > 0 and self.is_running():
            time.sleep(0.1)


