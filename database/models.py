import enum
import uuid
from datetime import datetime, timezone

from ext import pwd_context
from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def generate_uuid():
    return str(uuid.uuid4())


def generate_code():
    return str(uuid.uuid4())[:6].upper()


class BillType(enum.Enum):
    equal = 'equal'
    nonequal = 'nonequal'


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(String, default=generate_uuid, primary_key=True)

    username = mapped_column(String(50), nullable=False)
    _password = mapped_column("password", String(100), nullable=False)

    card = mapped_column(String, default=None, nullable=True)

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

    id = mapped_column(
        String(length=6), default=generate_code, primary_key=True)
    title = mapped_column(String, nullable=False)
    single = mapped_column(Boolean, default=False)

    def __str__(self) -> str:
        return self.title


class GroupMember(Base):
    __tablename__ = 'groupmember'

    group_id = mapped_column(ForeignKey(
        'groups.id', ondelete='CASCADE'), primary_key=True)
    group: Mapped['Group'] = relationship(lazy='subquery')

    member_id = mapped_column(ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    member: Mapped['User'] = relationship(lazy='subquery')

    def __str__(self) -> str:
        return f'{self.group} - {self.member}'


class Bill(Base):
    __tablename__ = 'bills'

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    title = mapped_column(String, nullable=False)

    type = mapped_column(Enum(BillType), nullable=False)

    group_id = mapped_column(ForeignKey(
        'groups.id', ondelete='CASCADE'), nullable=False)
    group: Mapped['Group'] = relationship(lazy='subquery')

    def __str__(self) -> str:
        return f'{self.title} - {self.group}'


class BillMember(Base):
    __tablename__ = 'billmember'

    bill_id = mapped_column(ForeignKey(
        'bills.id', ondelete='CASCADE'), primary_key=True)
    bill: Mapped['Bill'] = relationship(lazy='subquery')

    member_id = mapped_column(ForeignKey(
        'users.id', ondelete='CASCADE'), primary_key=True)
    member: Mapped['User'] = relationship(lazy='subquery')

    money = mapped_column(Float, default=0)
    dolg = mapped_column(Float, default=0)
    paid_dolg = mapped_column(Float, default=0)

    def __str__(self) -> str:
        return f'{self.member}'


class Product(Base):
    __tablename__ = 'position'

    id = mapped_column(String, default=generate_uuid, primary_key=True)
    bill_id = mapped_column(ForeignKey(
        'bills.id', ondelete='CASCADE'), nullable=False)
    bill: Mapped['Bill'] = relationship(lazy='subquery')

    price = mapped_column(Integer, nullable=False)
    name = mapped_column(String, nullable=False)

    quantity = mapped_column(Float, nullable=False)

    def __str__(self) -> str:
        return self.name
