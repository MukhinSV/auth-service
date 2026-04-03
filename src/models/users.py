import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    patronymic: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
