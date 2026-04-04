from fastapi import HTTPException


class AuthException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self) -> None:
        super().__init__(self.detail)


class PasswordNotConfirmedException(AuthException):
    detail = "Пароли не совпадают"


class UserAlreadyExistsException(AuthException):
    detail = "Пользователь с таким email уже существует"


class WrongEmailOrPasswordException(AuthException):
    detail = "Неверный логин или пароль"


class InvalidTokenException(AuthException):
    detail = "Неверный токен"


class ExpiredTokenException(AuthException):
    detail = "Токен истёк"


class NoDataForUpdateException(AuthException):
    detail = "Некорректные данные"


class UserNotFoundException(AuthException):
    detail = "Пользоваетль не найден"


class RoleNotFoundException(AuthException):
    detail = "Роль не найдена"


class RoleCanNotBeDeletedException(AuthException):
    detail = "Эта роль не может быть удалена"


class RoleAlreadyExistsException(AuthException):
    detail = "Такая роль уже существует"


class PermissionNotFoundException(AuthException):
    detail = "Разрешение не найдено"


class PermissionAlreadyExistsException(AuthException):
    detail = "Такое разрешение уже существует"


class ProductNotFoundException(AuthException):
    detail = "Товар не найден"


class AuthHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class PasswordNotConfirmedHTTPException(AuthHTTPException):
    status_code = 422
    detail = "Пароли не совпадают"


class UserAlreadyExistsHTTPException(AuthHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class WrongEmailOrPasswordHTTPException(AuthHTTPException):
    status_code = 401
    detail = "Неверный логин или пароль"


class UserUnauthorisedHTTPException(AuthHTTPException):
    status_code = 401
    detail = "Пользователь не аутентифицирован"


class InvalidTokenHTTPException(AuthHTTPException):
    status_code = 401
    detail = "Неверный токен"


class AccessDeniedHTTPException(AuthHTTPException):
    status_code = 403
    detail = "Доступ запрещён"


class NoDataForUpdateHTTPException(AuthHTTPException):
    status_code = 422
    detail = "Некорректные данные"


class UserNotFoundHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Пользоваетль не найден"


class RoleNotFoundHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Роль не найдена"


class RoleCanNotBeDeletedHTTPException(AuthHTTPException):
    status_code = 400
    detail = "Эта роль не может быть удалена"


class RoleAlreadyExistsHTTPException(AuthHTTPException):
    status_code = 409
    detail = "Такая роль уже существует"


class PermissionNotFoundHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Разрешение не найдено"


class PermissionAlreadyExistsHTTPException(AuthHTTPException):
    status_code = 409
    detail = "Такое разрешение уже существует"


class ProductNotFoundHTTPException(AuthHTTPException):
    status_code = 404
    detail = "Товар не найден"
