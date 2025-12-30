import uuid

from sqlalchemy import CHAR, String
from sqlalchemy.orm import Mapped, mapped_column

from arch_test.core.database import Base


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=lambda: uuid.uuid4().hex
    )
    login: Mapped[str] = mapped_column(String(15), unique=True)
    password: Mapped[str] = mapped_column(String(60))
