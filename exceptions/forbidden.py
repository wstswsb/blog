from .base_exception import BaseAppException


class Forbidden(BaseAppException):
    def __init__(self, value: dict, *args: object) -> None:
        super().__init__(*args)
        self.value = value
        self.code = 403
