import enum
import uuid
from datetime import datetime, timezone

from ext import pwd_context
from sqlalchemy import DateTime, Enum, ForeignKey, String, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


def generate_uuid():
    return str(uuid.uuid4())

class MemberStatusEnum(enum.Enum):
    creator = 'creator'
    member = 'member'


class BillTypeEnum(enum.Enum):
    equal = 'equal'
    cafe = 'cafe'
   # summary = 'summary'


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(String, default=generate_uuid, primary_key=True)

    username = mapped_column(String(50), nullable=False)
    _password = mapped_column("password", String(100), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __str__(self) -> str:
        return self.username


class Group(Base):
    __tablename__ = 'groups'

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    title = mapped_column(String, nullable=False)

    def __str__(self) -> str:
        return self.title


class GroupMember(Base):
    __tablename__ = 'groupmember'

    group_id = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True)
    group: Mapped['Group'] = relationship(lazy='subquery')

    member_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    member: Mapped['User'] = relationship(lazy='subquery')

    member_status = mapped_column(Enum(MemberStatusEnum), nullable=False)

    def __str__(self) -> str:
        return f'{self.group} - {self.member_status} - {self.member}'


class Bill(Base):
    __tablename__ = 'bills'

    id = mapped_column(String, default=generate_uuid, primary_key=True)

    title = mapped_column(String, nullable=False)

    group_id = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    group: Mapped['Group'] = relationship(lazy='subquery')

    payer_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    payer: Mapped['User'] = relationship(lazy='subquery')

    amount = mapped_column(Integer, nullable=False)
    type = mapped_column(Enum(BillTypeEnum), nullable=False)
    date = mapped_column(DateTime, nullable=False)

    def __str__(self) -> str:
        return f'{self.title} - {self.group} - {self.type}'
