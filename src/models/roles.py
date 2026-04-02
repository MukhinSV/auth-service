import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.users import UsersORM


class RolesORM(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list[UsersORM]] = relationship(
        back_populates="roles"
    )
