from typing import List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import between
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.database.models import Contact
from src.schemas import (
    ContactBase, ContactUpdate, ContactResponse, ContactUpdateFields
)


async def raise_contact_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Contact not found'
    )


async def get_contacts(
    skip: int,
    limit: int,
    db: Session
) -> List[ContactResponse]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(
    contact_id: int,
    db: Session
) -> ContactResponse:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contacts_by_name(
    name: Optional[str],
    db: Session
) -> List[ContactResponse]:
    return db.query(Contact).filter(Contact.name == name).all()


async def get_contacts_by_surname(
    surname: Optional[str],
    db: Session
) -> List[ContactResponse]:
    return db.query(Contact).filter(Contact.surname == surname).all()


async def get_contact_by_email(
    email: Optional[str],
    db: Session
) -> List[ContactResponse]:
    return db.query(Contact).filter(Contact.email == email).all()


async def create_contact(
    body: ContactBase,
    db: Session
) -> ContactResponse:
    body.birth_date = datetime.strptime(body.birth_date, '%d.%m.%Y')
    new_contact = Contact(**body.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    db: Session
) -> ContactResponse:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise_contact_not_found()

    try:
        body.birth_date = datetime.strptime(body.birth_date, '%d.%m.%Y')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid date format. Use dd.mm.yyyy'
        )
    for key, value in body.model_dump().items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact


async def update_contact_fields(
    contact_id: int,
    body: ContactUpdateFields,
    db: Session
) -> ContactResponse:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise_contact_not_found()
    for key, value in body.model_dump().items():
        if not value is None:
            setattr(contact, key, value)
    db.commit()
    return contact


async def delete_contact(
    contact_id: int,
    db: Session
) -> None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise_contact_not_found()
    if contact:
        db.delete(contact)
        db.commit()


async def get_birthdays(
    db: Session
) -> Optional[List[ContactResponse]]:
    contacts = db.query(Contact).filter(
        between(
            Contact.birth_date,
            datetime.now(timezone.utc),
            datetime.now(timezone.utc) + timedelta(days=7)
        )
    ).all()
    return contacts
