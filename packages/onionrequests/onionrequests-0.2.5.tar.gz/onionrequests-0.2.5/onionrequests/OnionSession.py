import random
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from onionrequests.TorPort import TorPort


class OnionSession(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Generate a unique username and password to connect to Tor.
        random.seed(time.time_ns())
        username = str(time.time_ns()) + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))
        password = str(time.time_ns()) + "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(10))

        # Figure out which port number Tor's SOCKS proxy is using, if available.
        port = TorPort.get_tor_port()

        # Tell the session to use HTTP through a Tor proxy.
        retry = Retry(connect=10, backoff_factor=1.0)
        adapter = HTTPAdapter(max_retries=retry)
        self.mount('http://', adapter)
        self.mount('https://', adapter)
        self.proxies = {
            'http': 'socks5://{}:{}@localhost:{}'.format(username, password, port),
            'https': 'socks5://{}:{}@localhost:{}'.format(username, password, port)
        }
