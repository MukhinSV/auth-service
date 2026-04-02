import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.roles import RolesORM


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    roles: Mapped[RolesORM] = relationship(
        back_populates="users"
    )
