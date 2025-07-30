

class CouldNotFindTorPortException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = "Could not connect to Tor using the expected ports. Is Tor installed on this machine?"
        super().__init__(message)

