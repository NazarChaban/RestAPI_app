from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


# Contact schemas
class ContactModel(BaseModel):
    name: str = Field(max_length=150)
    surname: str = Field(max_length=150)
    email: str = Field(max_length=150)
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
    name: Optional[str] = Field(max_length=150)
    surname: Optional[str] = Field(max_length=150)
    email: Optional[str] = Field(max_length=150)
    phone_number: Optional[str] = Field(max_length=50)


# User schemas
class UserModel(BaseModel):
    username: str = Field(max_length=150)
    email: str
    password: str = Field(min_length=8, max_length=22)


class UserDB(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDB
    detail: str = 'User created successfully'


# Token schemas
class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


# Email schemas
class RequestEmail(BaseModel):
    email: EmailStr
