from fastapi import FastAPI
import uvicorn

from src.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/api")

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
    "phone_number": "1234567891"
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
"""