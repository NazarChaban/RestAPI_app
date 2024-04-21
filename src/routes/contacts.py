from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
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
    status_code=status.HTTP_201_CREATED
)
async def create_contact(
    body: ContactBase,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    return await repository_contacts.create_contact(body, curr_user, db)


@router.get('/', response_model=List[ContactResponse])
async def get_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
    return await repository_contacts.get_contacts(skip, limit, curr_user, db)


@router.get('/search', response_model=List[ContactResponse])
async def search_contact(
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
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
    response_model=List[ContactResponse]
)
async def get_birthdays(
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> List[ContactResponse]:
    return await repository_contacts.get_birthdays(curr_user, db)


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    contact = await repository_contacts.get_contact(contact_id, curr_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found'
        )
    return contact


@router.put(
    '/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
async def update_contact(
    contact_id: int,
    body: ContactUpdate,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    return await repository_contacts.update_contact(
        contact_id, body, curr_user, db
    )


@router.patch(
    '/{contact_id}',
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
async def update_contact_fields(
    contact_id: int,
    body: ContactUpdateFields,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> ContactResponse:
    return await repository_contacts.update_contact_fields(
        contact_id, body, curr_user, db
    )


@router.delete(
    '/{contact_id}',
    status_code=status.HTTP_200_OK
)
async def delete_contact(
    contact_id: int,
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
) -> None:
    await repository_contacts.delete_contact(contact_id, curr_user, db)
