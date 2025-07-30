class TelerException(Exception):
    message = "An exception occurred."
    code = 500

    def __init__(self, msg: str = message):
        super().__init__(msg)


class BadParameters(TelerException):
    message = "Bad Parameter"
    code = 400

    def __init__(self, param: str = "", msg: str = message):
        self.param = param
        super().__init__(msg)


class NotImplemented(TelerException):
    message = "Not implemented"
    code = 501

    def __init__(self, msg: str = message):
        super().__init__(msg)
