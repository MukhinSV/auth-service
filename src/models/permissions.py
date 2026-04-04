import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.roles import RolesORM


class PermissionsORM(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str | None] = mapped_column(nullable=True)
    roles: Mapped[list["RolesORM"]] = relationship(
        back_populates="permissions",
        secondary="roles_permissions",
    )
