import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, mapped_column

from ext import pwd_context


def generate_uuid():
    return str(uuid.uuid4())


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(String, default=generate_uuid, primary_key=True)

    username = mapped_column(String(50), nullable=False, primary_key=True)
    _password = mapped_column("password", String(100), nullable=False)

    registered_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)
