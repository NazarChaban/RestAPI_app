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
    """
    The lifespan function is a coroutine that runs before and after the
    application.
    It's used to initialize and close resources, such as database connections.

    :param app: Pass the fastapi instance to the function
    :return: An object that can be used to clean up the resources when the server shuts down
    """
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
    """
    The read_root function returns a dictionary with the key 'message' and
    value &quot;Contact manager API&quot;.

    :return: A dictionary
    """
    return {'message': "Contact manager API"}


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
