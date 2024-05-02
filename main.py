from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
from fastapi import FastAPI
import uvicorn

from src.routes import contacts, auth, users
from src.conf.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    r = await aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0
    )
    await FastAPILimiter.init(r)
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix='/api')

origins = [
    'http://contact-manager.com/frontend',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    return {'message': "Contact manager API"}

if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )

"""
 - GET /api/contacts

AUTHORIZATION:

 - POST /api/auth/signup
{
    "username": "test",
    "email": "test@api.com",
    "password": "123456789"
}

 - POST /api/auth/login
{
    "username": "test@api.com",
    "password": "123456789"
}
Header:
Authorization: Bearer {access_token} (from response)

 - POST /api/contacts
{
    "name": "John",
    "surname": "Doe",
    "email": "test@api.com",
    "phone_number": "123456789",
    "birth_date": "18.04.2024",
    "additional_info": "test"
}

 - GET /api/contacts/{id}
 - PUT /api/contacts/{id}
{
    "name": "John0",
    "surname": "Doe0",
    "email": "test1@api.com",
    "phone_number": "1234567891",
    "birth_date": "21.04.2024",
    "additional_info": "test1"
}
 - PATCH /api/contacts/{id}
{
    "name": "John1",
    "surname": "Doe1",
    "email": null,
    "phone_number": null
}
 - DELETE /api/contacts/{id}

 - GET /api/contacts/search?name=John1
 - GET /api/contacts/search?surname=Doe1
 - GET /api/contacts/search?email=test1@api.com

 - GET /api/contacts/birthdays

 - GET /api/auth/confirmed_email/{token}
 - POST /apiauth/request_email

 - GET /api/users/me
 - PATCH /api/users/avatar
"""