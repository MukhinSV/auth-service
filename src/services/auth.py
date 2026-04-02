from src.exceptions import PasswordsNotEqualException
from src.schemas.users import UserRegisterRequest
from src.services.base import BaseService


class AuthService(BaseService):
    @staticmethod
    def check_equal_password_and_repeated_password(
            password: str,
            repeated_password: str
    ) -> bool:
        if password == repeated_password:
            return True
        return False

    async def register(self, user_data: UserRegisterRequest):
        if not self.check_equal_password_and_repeated_password(
                user_data.password,
                user_data.repeated_password
        ):
            raise PasswordsNotEqualException
