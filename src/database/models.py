from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, String
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

from src.database.db import engine

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    surname: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    additional_info: Mapped[str | None]


Base.metadata.create_all(engine)
