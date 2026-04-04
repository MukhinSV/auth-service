from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class UsersRolesORM(Base):
    __tablename__ = "users_roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
