class InferenceException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MaitaiConnectionError(ConnectionError):
    def __init__(self, msg: str):
        super().__init__(msg)


class BadRequestError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class NotFoundError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InferenceWarning(Warning):
    def __init__(self, *args, **kwargs):
        pass
