from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, String, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

from src.database.db import engine

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    surname: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True
    )
    phone_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    additional_info: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), default=None
    )
    user: Mapped['User'] = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    refresh_token: Mapped[str | None]


Base.metadata.create_all(engine)
