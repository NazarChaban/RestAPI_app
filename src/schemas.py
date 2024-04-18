from datetime import datetime, timedelta, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)
    birth_date: datetime
    additional_info: Optional[str]


class ContactBase(ContactModel):
    birth_date: str


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True


class ContactUpdate(ContactModel):
    birth_date: str


class ContactUpdateFields(BaseModel):
    name: Optional[str] = Field(max_length=50)
    surname: Optional[str] = Field(max_length=50)
    email: Optional[str] = Field(max_length=50)
    phone_number: Optional[str] = Field(max_length=50)
