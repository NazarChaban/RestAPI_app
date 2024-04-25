from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDB

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/me', response_model=UserDB)
async def read_users_me(
    curr_user: User = Depends(auth_service.get_current_user)
):
    return curr_user


@router.patch('/avatar', response_model=UserDB)
async def update_avatar(
    file: UploadFile = File(),
    curr_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
    )
    resp = cloudinary.uploader.upload(
        file.file,
        public_id=f'ContactManager/{curr_user.username}',
        overwrite = True
    )
    src_url = cloudinary.CloudinaryImage(
        f'ContactManager/{curr_user.username}'
    ).build_url(
        width=250, height=250, crop='fill', version=resp.get('version')
    )
    return await repository_users.update_avatar(curr_user.email, src_url, db)
