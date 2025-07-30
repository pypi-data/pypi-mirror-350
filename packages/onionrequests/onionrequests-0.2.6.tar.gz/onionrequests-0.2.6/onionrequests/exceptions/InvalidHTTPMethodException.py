

class InvalidHTTPMethodException(Exception):
    def __init__(self, message: str = None, invalid_method: str = None):
        if message is None:
            message = "An invalid HTTP method was provided to the OnionQueue"
            if isinstance(invalid_method, str):
                message += ": {}. ".format(invalid_method)
            else:
                message += ". "
            message += "Valid HTTP methods include: GET, HEAD, POST, PUT, DELETE, OPTIONS, or PATCH."
        super().__init__(message)


