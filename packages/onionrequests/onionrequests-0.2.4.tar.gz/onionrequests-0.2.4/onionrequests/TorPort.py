import socket

from onionrequests.exceptions import CouldNotFindTorPortException


class TorPort:
    __CONST_TOR_PORT = None

    # If your Tor port isn't in this list, you can append it.
    # The first valid port found from this list is assumed to be the Tor SOCKS port.
    __potential_tor_ports = [
        9050,  # Default for Linux.
        9150,  # Default for Windows.
    ]

    @classmethod
    def get_tor_port(cls) -> int:
        if isinstance(cls.__CONST_TOR_PORT, int):
            return cls.__CONST_TOR_PORT

        for port_num in cls.__potential_tor_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", port_num))
                cls.__CONST_TOR_PORT = port_num
                return port_num
            except:
                continue

        raise CouldNotFindTorPortException()

    @classmethod
    def add_potential_tor_port(cls, port_num: int):
        assert isinstance(port_num, int)
        cls.__potential_tor_ports.insert(0, port_num)
