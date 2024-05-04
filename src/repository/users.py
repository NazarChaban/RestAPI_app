from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(
    email: str,
    db: Session
) -> User:
    """
    The get_user_by_email function returns a user object from the database
    based on the email address provided.

    :param email: Pass the email of a user to the function
    :param db: Pass the database session to the function
    :return: The first user that matches the email address
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(
    body: UserModel,
    db: Session
) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: Specify the type of data that is expected to be passed into the function
    :param db: Access the database
    :return: A user object
    """
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(
    user: User,
    token: str | None,
    db: Session
) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: Identify the user in the database
    :param token: Update the user's refresh token
    :param db: Commit the changes to the database
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(
    email: str,
    db: Session
) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.

    :param email: Get the email of the user
    :param db: Create a database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(
    email: str,
    url: str,
    db: Session
) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Identify the user in the database
    :param url: Get the url of the avatar from the request body
    :param db: Pass the database session to the function
    :return: The updated user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
