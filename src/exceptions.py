from fastapi import HTTPException


class AuthException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self) -> None:
        super().__init__(self.detail)


class PasswordsNotEqualException(AuthException):
    detail = "Пароли не совпадают"


class AuthHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class PasswordsNotEqualHTTPException(AuthHTTPException):
    status_code = 422
    detail = "Пароли не совпадают"
