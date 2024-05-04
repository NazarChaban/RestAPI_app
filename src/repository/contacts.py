from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy import between, and_
from sqlalchemy.orm import Session
from typing import List, Optional

from src.schemas import (
    ContactBase, ContactUpdate, ContactResponse, ContactUpdateFields
)
from src.database.models import Contact, User


async def raise_contact_not_found():
    """
    The raise_contact_not_found function raises a 404 Not Found error with the
    message 'Contact not found'.

    :return: A response object with the status code 404 and a detail message
    """
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Contact not found'
    )


async def get_contacts(
    skip: int,
    limit: int,
    user: User,
    db: Session
) -> List[ContactResponse]:
    """
    The get_contacts function returns a list of contacts for the user.
    The function takes in three parameters: skip, limit, and user.
    Skip is an integer that determines how many contacts to skip over
    before returning results.
    Limit is an integer that determines how many results to return after
    skipping over the specified number of contacts.
    User is a User object containing information about the current
    logged-in user.

    :param skip: Skip the first n contacts
    :param limit: Limit the number of contacts returned
    :param user: Get the user_id from the user object
    :param db: Pass the database session to the function
    :return: A list of contacts
    """
    return db.query(Contact).filter(
        Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(
    contact_id: int,
    user: User,
    db: Session
) -> ContactResponse:
    """
    The get_contact function returns a single contact from the database.

    :param contact_id: Specify the id of the contact we want to get
    :param user: Check if the user is authorized to access the contact
    :param db: Access the database
    :return: A ContactResponse object
    """
    return db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()


async def get_contacts_by_name(
    name: Optional[str],
    user: User,
    db: Session
) -> List[ContactResponse]:
    """
    The get_contacts_by_name function returns a list of contacts that match
    the name parameter.
    If no name is provided, all contacts are returned.

    :param name: Filter the contacts by name
    :param user: Get the user_id from the user object
    :param db: Connect to the database
    :return: A list of contacts that match the name and user_id
    """
    return db.query(Contact).filter(
        and_(Contact.name == name, Contact.user_id == user.id)).all()


async def get_contacts_by_surname(
    surname: Optional[str],
    user: User,
    db: Session
) -> List[ContactResponse]:
    """
    The get_contacts_by_surname function returns a list of contacts with the
    given surname.

    :param surname: Define the type of data that will be passed into the function
    :param user: Get the user id from the database
    :param db: Pass the database session to the function
    :return: A list of contactresponse objects
    """
    return db.query(Contact).filter(
        and_(Contact.surname == surname, Contact.user_id == user.id)).all()


async def get_contact_by_email(
    email: Optional[str],
    user: User,
    db: Session
) -> List[ContactResponse]:
    """
    The get_contact_by_email function returns a list of contacts that match
    the email address provided.
    If no email is provided, all contacts are returned.

    :param email: Filter the query by email
    :param user: Get the user id of the logged in user
    :param db: Connect to the database
    :return: A list of contacts
    """
    return db.query(Contact).filter(
        and_(Contact.email == email, Contact.user_id == user.id)).all()


async def create_contact(
    body: ContactBase,
    user: User,
    db: Session
) -> ContactResponse:
    """
    The create_contact function creates a new contact in the database.

    :param body: Define the type of data that is expected to be passed in
    :param user: Get the user id from the token
    :param db: Pass the database session to the function
    :return: A contactresponse object
    """
    body.birth_date = datetime.strptime(body.birth_date, '%d.%m.%Y')
    new_contact = Contact(**body.model_dump(), user=user)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    user: User,
    db: Session
) -> ContactResponse:
    """
    The update_contact function updates a contact in the database.

    :param contact_id: Identify the contact to be updated
    :param body: Pass the data from the request body to the function
    :param user: Get the user id of the current logged in user
    :param db: Access the database
    :return: A contactresponse object
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
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
    user: User,
    db: Session
) -> ContactResponse:
    """
    The update_contact_fields function updates the fields of a contact.

    :param contact_id: Find the contact in the database
    :param body: Pass the data from the request body to this function
    :param user: Get the user id of the current logged in user
    :param db: Create a database session
    :return: The updated contact
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact is None:
        raise_contact_not_found()
    for key, value in body.model_dump().items():
        if value is not None:
            setattr(contact, key, value)
    db.commit()
    return contact


async def delete_contact(
    contact_id: int,
    user: User,
    db: Session
) -> None:
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: Identify the contact to be deleted
    :param user: Get the user id from the database
    :param db: Connect to the database
    :return: None
    """
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact is None:
        raise_contact_not_found()
    if contact:
        db.delete(contact)
        db.commit()


async def get_birthdays(
    user: User,
    db: Session
) -> Optional[List[ContactResponse]]:
    """
    The get_birthdays function returns a list of contacts with birthdays in
    the next 7 days.

    :param user: Get the user id
    :param db: Pass the database session into the function
    :return: A list of contacts that have a birthday within the next 7 days
    """
    contacts = db.query(Contact).filter(
        and_(
            between(
                Contact.birth_date,
                datetime.now(timezone.utc),
                datetime.now(timezone.utc) + timedelta(days=7)
            ),
            Contact.user_id == user.id
        )
    ).all()
    return contacts
