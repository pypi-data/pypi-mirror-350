from package.app.utilities.enum import SpecialExceptionCodeEnum


class CustomHTTPException(Exception):
    def __init__(
        self,
        message: str,
        errors: dict = {},
        status_code: int = 400,
        special_code: int = SpecialExceptionCodeEnum.NORMAL_ERROR,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.errors = errors
        self.special_code = special_code
