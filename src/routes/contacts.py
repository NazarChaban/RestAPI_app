from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.schemas import (
    ContactBase, ContactResponse, ContactUpdate, ContactUpdateFields
)
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User
from src.database.db import get_db

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.post(
    '/',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def create_contact(
    body: ContactBase,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    The create_contact function creates a new contact in the database.

    :param body: Get the data from the request body
    :param curr_user: Get the user that is currently logged in
    :param db: Pass the database session to the repository layer
    :return: A contactresponse object
    """
    return await repository_contacts.create_contact(body, curr_user, db)


@router.get(
    '/', response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
    """
    The get_contacts function returns a list of contacts for the current user.

    :param skip: Skip a certain amount of contacts
    :param limit: Limit the number of contacts returned
    :param curr_user: Get the current user from the auth_service
    :param db: Pass the database session to the repository layer
    :return: A list of contactresponse objects
    """
    return await repository_contacts.get_contacts(skip, limit, curr_user, db)


@router.get(
    '/search', response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def search_contact(
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
    """
    The search_contact function allows the user to search for contacts by
    name, surname or email.

    :param name: Specify that the name parameter is optional
    :param surname: Get the surname from the query string
    :param email: Search for a contact by email
    :param curr_user: Get the current user
    :param db: Pass the database session to the function
    :return: A list of contactresponse objects, depending on the query parameters
    """
    if name is not None:
        return await repository_contacts.get_contacts_by_name(
            name, curr_user, db
        )
    if surname is not None:
        return await repository_contacts.get_contacts_by_surname(
            surname, curr_user, db
        )
    if email is not None:
        return await repository_contacts.get_contact_by_email(
            email, curr_user, db
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='At least one query parameter must be provided'
    )


@router.get(
    '/birthdays',
    response_model=List[ContactResponse],
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def get_birthdays(
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
    """
    The get_birthdays function returns a list of contacts that have birthdays
    in the current month.

    :param curr_user: Get the current user
    :param db: Pass the database connection to the repository layer
    :return: A list of contactresponse objects
    """
    return await repository_contacts.get_birthdays(curr_user, db)


@router.get(
    '/{contact_id}', response_model=ContactResponse,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def get_contact(
    contact_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    The get_contact function returns a single contact from the database.

    :param contact_id: Identify the contact to be retrieved
    :param curr_user: Get the current user from the database
    :param db: Get the database session
    :return: A contactresponse object
    """
    contact = await repository_contacts.get_contact(contact_id, curr_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found'
        )
    return contact


@router.put(
    '/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    The update_contact function updates a contact in the database.

    :param contact_id: Identify the contact to be updated
    :param body: Get the contact information from the request body
    :param curr_user: Get the current user
    :param db: Access the database
    :return: A contactresponse object
    """
    return await repository_contacts.update_contact(
        contact_id, body, curr_user, db
    )


@router.patch(
    '/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def update_contact_fields(
    contact_id: int,
    body: ContactUpdateFields,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    The update_contact_fields function updates the fields of a contact.

    :param contact_id: Identify the contact to be updated
    :param body: Pass the data from the request body to the function
    :param curr_user: Get the current user from the auth_service
    :param db: Pass the database session to the repository
    :return: A contactresponse object
    """
    return await repository_contacts.update_contact_fields(
        contact_id, body, curr_user, db
    )


@router.delete(
    '/{contact_id}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def delete_contact(
    contact_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: Specify the id of the contact that is to be deleted
    :param curr_user: Get the current user from the token
    :param db: Pass the database session to the repository layer
    :return: None
    """
    await repository_contacts.delete_contact(contact_id, curr_user, db)
