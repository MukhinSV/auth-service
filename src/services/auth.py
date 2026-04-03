from datetime import datetime, timezone, timedelta

import jwt
from fastapi import Response
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import PasswordNotConfirmedException, \
    UserAlreadyExistsException, WrongEmailOrPasswordException, \
    InvalidTokenException, ExpiredTokenException
from src.schemas.roles import RoleRequest
from src.schemas.users import UserRegisterRequest, User, UserRegister, \
    UserUpdatePartly, UserLoginRequest
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    access_cookie_key = "access_token"
    refresh_cookie_key = "refresh_token"
    access_token_type = "access"
    refresh_token_type = "refresh"

    @staticmethod
    def check_password_confirmation(
            password: str,
            password_confirmation: str
    ) -> None:
        if password != password_confirmation:
            raise PasswordNotConfirmedException

    async def check_user_existence(self, email: str) -> User:
        user = await self.db.users.get_one_or_none(email=email)
        if user and user.is_active:
            raise UserAlreadyExistsException
        return user

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    @staticmethod
    def create_token(data: dict) -> str:
        encoded_jwt = jwt.encode(
            data, settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire, "type": self.access_token_type}
        return self.create_token(to_encode)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            hours=settings.REFRESH_TOKEN_EXPIRE_HOURS
        )
        to_encode |= {"exp": expire, "type": self.refresh_token_type}
        return self.create_token(to_encode)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise InvalidTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    def decode_access_token(self, token: str) -> dict:
        payload = self.decode_token(token)
        if payload.get("type") != self.access_token_type:
            raise InvalidTokenException
        return payload

    def decode_refresh_token(self, token: str) -> dict:
        payload = self.decode_token(token)
        if payload.get("type") != self.refresh_token_type:
            raise InvalidTokenException
        return payload

    def issue_tokens(self, user_id: int) -> dict[str, str]:
        return {
            "access_token": self.create_access_token({"user_id": user_id}),
            "refresh_token": self.create_refresh_token({"user_id": user_id}),
        }

    @staticmethod
    def _set_cookie(
            response: Response,
            key: str,
            value: str,
            max_age: int,
    ) -> None:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=max_age,
            path="/",
        )

    @classmethod
    def set_auth_cookies(cls, response: Response, tokens: dict[str, str]) -> None:
        cls._set_cookie(
            response=response,
            key=cls.access_cookie_key,
            value=tokens["access_token"],
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        cls._set_cookie(
            response=response,
            key=cls.refresh_cookie_key,
            value=tokens["refresh_token"],
            max_age=settings.REFRESH_TOKEN_EXPIRE_HOURS * 60 * 60,
        )

    @classmethod
    def clear_auth_cookies(cls, response: Response) -> None:
        response.delete_cookie(cls.access_cookie_key, path="/")
        response.delete_cookie(cls.refresh_cookie_key, path="/")

    async def register(self, user_data: UserRegisterRequest) -> User:
        self.check_password_confirmation(
            user_data.password,
            user_data.password_confirmation
        )
        user = await self.check_user_existence(user_data.email)
        if user is None:
            user_data_for_add = UserRegister(
                **user_data.model_dump(
                    exclude={"password", "password_confirmation"}),
                hashed_password=self.hash_password(user_data.password)
            )
            user_res = await self.db.users.add(user_data_for_add)
            await self.db.roles.add(
                RoleRequest(user_id=user_res.id),
                exclude_unset=True
            )
        else:
            user_res = await self.db.users.update(
                UserUpdatePartly(is_active=True),
                exclude_unset=True,
                id=user.id
            )
        await self.db.commit()
        return user_res

    async def login(self, user_data: UserLoginRequest) -> dict:
        user = await self.db.users.get_user_with_hashed_password(
            email=user_data.email)
        if not user:
            raise WrongEmailOrPasswordException
        if not self.verify_password(user_data.password, user.hashed_password):
            raise WrongEmailOrPasswordException
        return self.issue_tokens(user.id)

    def refresh(self, refresh_token: str) -> dict[str, str]:
        refresh_token_data = self.decode_refresh_token(refresh_token)
        return self.issue_tokens(refresh_token_data["user_id"])
