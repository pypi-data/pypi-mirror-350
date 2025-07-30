# OnionRequests

The OnionRequests package is designed to allow for simple and anonymous HTTP requests using the Tor network.

---

## Setup

OnionRequests requires Tor to be installed on the machine running its code. This does not include the host machine if running inside a virtual machine, Docker container, etc. -- the guest machine should still be able to connect to Tor.

If your working machine is Linux, you can install the "tor" package through the terminal.

```bash
sudo apt-get install -y tor
```

If you are using Windows, you can download and install Tor here:

```text
https://www.torproject.org/download/
```

---

## Using the OnionSession Class

The OnionSession class inherits code from the requests.Session class, and can therefore be used in similar ways. The main difference is that OnionSession automatically connects to a Tor proxy upon initialization.

Here is an example of the class being used to make a GET request:

```python
from onionrequests import OnionSession


if __name__ == "__main__":
    session = OnionSession()

    url = "https://example.com/"
    with session.get(url) as res:
        res.raise_for_status()

        # Your code here...
```

And another example of the class being used to make a POST request:

```python
from onionrequests import OnionSession


if __name__ == "__main__":
    session = OnionSession()

    url = "https://example.com/"
    data = {"A": 1, "B": 2, "C": 3}
    with session.post(url, json=data) as res:
        res.raise_for_status()

        # Your code here...
```

---

## Queuing Tor Requests Using the OnionQueue Class

It is sometimes beneficial to run multiple OnionSession objects concurrently, since a large number of requests can be split between multiple public-facing IPv4 addresses. The package comes with a class called OnionQueue that handles a queue of requests concurrently using multithreading.

Below is an example of how it might be implemented:

```python
from requests import Response
from onionrequests import OnionQueue
from onionrequests import OnionSession


def handler(res: Response, session: OnionSession, download_path: str):
    res.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(res.content)


if __name__ == "__main__":
    onion_queue = OnionQueue()

    download_src_urls = [
        # A list of PNG image source urls to download.
    ]
    for x, url in enumerate(download_src_urls, start=1):
        req_kwargs = {"download_path": f"{x}.png", }
        onion_queue.add_task(
            url,
            response_handler=handler,
            req_kwargs=req_kwargs
        )

    onion_queue.start()
    onion_queue.wait_for_tasks()
```

### OnionQueue Class Initialization

| Argument                  | Default | Description                                                                                                                                                                                                   |
| ------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| sessions                  | None    | An optional list of OnionSession objects that will be used to make requests. The default is None, which means the class will create its own.                                                                  |
| num_threads               | 3       | The number of threads to run concurrently while processing tasks in the queue. If there are fewer OnionSession objects provided upon initialization, the class will create one for each thread automatically. |
| balance_session_requests  | True    | A boolean indicating whether or not to throttle sessions so that tasks are more-evenly distributed across all threads. For more information, check the set_balance_error_multiplier() class method section.   |
| wait_time_s_after_request | 0.25    | Time in seconds between each request made by the same session.                                                                                                                                                |

None of the arguments used for OnionQueue initialization are required.

### OnionQueue.add_task()

***Return type: None***

Individual tasks can be added to the queue using the OnionQueue.add_task() method. Arguments for this method are as follows:

| Argument         | Description                                                                                                                                                                                                                                           |
|:-----------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| url              | The URL passed to OnionSession.get() or OnionSession.post().                                                                                                                                                                                          |
| response_handler | A reference to the function that handles the session's response (more information below).                                                                                                                                                             |
| method           | A string representing the type of request made by OnionSession. Can be one of the following: GET, HEAD, POST, PUT, DELETE, OPTIONS, or PATCH. Default is GET.                                                                                         |
| req_args         | A list of arguments passed to OnionSession.get() or OnionSession.post().                                                                                                                                                                              |
| req_kwargs       | A dictionary of keyword arguments passed to OnionSession.get() or OnionSession.post().                                                                                                                                                                |
| handler_args     | A list of arguments passed to the response handler after a request has been made. This is helpful for passing additional context (such as a download path) to the response handler that cannot be obtained through the response itself.               |
| handler_kwargs   | A dictionary of keyword arguments passed to the response handler after a request has been made. This is helpful for passing additional context (such as a download path) to the response handler that cannot be obtained through the response itself. |

### The Response Handler Function

Use cases may vary, so it is up to the developer to describe how a response should be handled after a request is made.

There are two arguments that are always passed from the OnionQueue to the response handler: the first for the response to be handled, and the second for the session (OnionSession) that made the request. The OnionSession object is passed in case it should be accessed during the processing of the response, or in case the original request failed somehow and should be retried.

```python
from requests import Response
from onionrequests import OnionSession

# Here is an example request handler that saves binary data to a file.
def handler(res: Response, session: OnionSession, download_path: str):
    res.raise_for_status()
    with open(download_path, 'wb') as file:
        file.write(res.content)
```

While working with OnionQueue response handlers, be aware of the following:

- Responses are not checked for status code 200 inside the OnionQueue. This is so that if the request fails somehow, it can be handled (or retried) inside of the response handler.

- Raising an uncaught exception from inside the response handler will stop the queue before re-raising the exception. If one thread's response handler raises an exception, all threads should stop.

- The OnionQueue class does not expect any value to be returned from the response handler. If one is returned, the OnionQueue class will ignore it.

### OnionQueue.clear_task_queue()

***Return type: None***

This method empties out the task queue. If OnionQueue.is_running() is True, then an exception is raised because the method cannot clear the queue while tasks are ongoing.

### OnionQueue.is_running()

***Return type: bool***

Returns True if the OnionQueue object is currently processing tasks or is waiting for new tasks to be added to an empty queue, or False otherwise.

Calling OnionQueue.start() sets this to True immediately, while encountering an exception during task processing or calling OnionQueue.stop() sets this to False once tasks have halted.

### OnionQueue.num_tasks_remaining()

***Return type: int***

Returns an integer greater than or equal to zero for the number of tasks left in the queue. This includes tasks that have not yet started as well as those in progress.

### OnionQueue.set_balance_error_multiplier()

***Return type: None***

| Argument       | Description                                      |
|:--------------:| ------------------------------------------------ |
| new_multiplier | Any float or integer greater than or equal to 0. |

To minimize the number of requests any one OnionSession makes, the OnionQueue class attempts to spread out tasks between them in a somewhat even manner.

The way this works is by tracking the number of requests each OnionSession makes, then temporarily pausing any that make too many above the average. The provided (or default) multiplier is used to calculate an error range above the session request average. If the number of session requests is below the average plus error, the session is allowed to make another request. If above, the session is paused until other sessions raise the average.

Here is some Python code to help describe how this works:

```python
session_request_nums = [
    # List of integers tracking request counts.
]

# Calculate average number of requests between all OnionSession objects.
avg_num_requests = sum(session_request_nums) / len(session_request_nums)

# Calculate an error range based on the multiplier and number of threads.
allowed_error = current_balance_error_multiplier * num_threads

# While this session has made too many requests above the average, wait.
while current_session_request_num > avg_num_requests + allowed_error:
    time.sleep(0.1)
```

If you would like a perfectly even split of tasks between OnionSession objects, setting a balance multiplier of 0 will remove the error and pause any thread with an above average request count. Be cautious when working with large downloads though, as they may cause unwanted delays in other threads during task processing.

There is a way to disable this feature, if desired, to allow each thread to make as many requests as possible without limitation. During OnionQueue initialization, setting the "balance_session_requests" argument to False will skip this check and allow threads to continue regardless of OnionSession request counts.

### OnionQueue.start()

***Return type: None***

The OnionQueue class does not begin processing tasks until after the start method has been called. Once called, the start method will launch the desired number of threads (specified at class initialization) to empty out the queue. After all threads have been started, the method returns without pausing.

### OnionQueue.stop()

***Return type: None***

Once started, the OnionQueue class does not stop processing queued tasks until the stop method has been called, even if the queue is empty. Calling the stop method prevents the OnionQueue class from starting any new tasks.

Note that calling OnionQueue.stop() does not immediately stop any ongoing tasks. Those tasks continue until they finish or raise an exception, then the thread ends before the next task can start.

### OnionQueue.wait_for_tasks()

***Return type: None***

This method just halts the current thread until all tasks have been processed, or until the queue is no longer processing tasks (i.e. stop() was called or an exception was raised).

---

## Exceptions

### CouldNotFindTorPortException

Getting this error means that the program wasn't able to automatically determine which port number Tor is using as a SOCKS proxy. If you encounter this exception, here are some steps for debugging:
1. Check to make sure Tor is installed on the machine running the code. If the program is running inside of a Docker container or virtual machine, installing Tor on the guest machine is the simplist solution to this problem. Alternatively, you might be able to configure your networking settings to redirect the guest machine's traffic through the host machine's Tor.
2. If Tor is installed and you are running on Windows, try again while the Tor browser is open.
3. If you know the port number for your Tor SOCKS proxy, you can add it at the start of your code like this:
    ```python
    from onionrequests.TorPort import TorPort
    from onionrequests import OnionSession
    
    if __name__ == "__main__":
        port_num = 1234
        TorPort.add_potential_tor_port(port_num)
        
        # Your code here...
    ```
    By default, the program checks port 9050 for Linux and 9150 for Windows.
