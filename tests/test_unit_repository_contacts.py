import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.repository.contacts import (
    get_contacts, get_contact, get_contacts_by_name,
    get_contacts_by_surname, get_contact_by_email, create_contact,
    update_contact, update_contact_fields, delete_contact,
    get_birthdays, HTTPException
)
from src.schemas import (
    ContactBase, ContactUpdate, ContactUpdateFields
)
from src.database.models import Contact, User


class TestContacts(unittest.TestCase):
    def setUp(self):
        self.session: Session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.mock_contacts = [
            Contact(
                id=1, name="John", surname="Doe", email="john@example.com",
                phone_number="12345", birth_date='04.05.1990'
            )
        ]

    async def test_get_contacts(self):
        self.session.query().filter().offset().limit().all.return_value = self.mock_contacts
        contacts = await get_contacts(
            skip=0, limit=10, user=self.user, db=self.session
        )
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.mock_contacts[0])

    async def test_get_contact(self):
        self.session.query().filter().first.return_value = self.mock_contacts[0]
        contact = await get_contact(
            contact_id=1, user=self.user, db=self.session
        )
        self.assertIsNotNone(contact)
        self.assertEqual(contact, self.mock_contacts[0])

    async def test_get_contacts_by_name(self):
        self.session.query().filter().all.return_value = self.mock_contacts
        contacts = await get_contacts_by_name(
            name="John", user=self.user, db=self.session
        )
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.mock_contacts[0])

    async def test_get_contacts_by_surname(self):
        self.session.query().filter().all.return_value = self.mock_contacts
        contacts = await get_contacts_by_surname(
            surname="Doe", user=self.user, db=self.session
        )
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.mock_contacts[0])

    async def test_get_contact_by_email(self):
        self.session.query().filter().all.return_value = self.mock_contacts
        contacts = await get_contact_by_email(
            email="john@example.com", user=self.user, db=self.session
        )
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0], self.mock_contacts[0])

    async def test_create_contact(self):
        contact_data = ContactBase(
            name="John", surname="Doe", email="john@example.com",
            phone_number="12345", birth_date='04.05.1990'
        )
        new_contact = await create_contact(
            body=contact_data, user=self.user, db=self.session
        )
        self.assertEqual(new_contact, self.mock_contacts[0])

    async def test_update_contact(self):
        contact_data = ContactUpdate(
            name="John1", surname="Doe1", email="john1@example.com",
            phone_number="123451", birth_date='04.05.1990'
        )
        self.session.query().filter().first.return_value = self.mock_contacts[0]
        updated_contact = await update_contact(
            contact_id=1, body=contact_data, user=self.user, db=self.session
        )
        self.assertEqual(updated_contact.name, "John1")
        self.assertEqual(updated_contact.surname, "Doe1")
        self.assertEqual(updated_contact.email, "john1@example.com")

    async def test_update_contact_None(self):
        contact_data = ContactUpdate(
            name="John1", surname="Doe1", email="john1@example.com",
            phone_number="123451", birth_date='04.05.1990'
        )
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException):
            await update_contact(
                contact_id=1, body=contact_data,
                user=self.user, db=self.session
            )

    async def test_update_contact_fields(self):
        contact_data = ContactUpdateFields(
            name="John1", surname="Doe1", email="john1@example.com",
            phone_number="123451"
        )
        self.session.query().filter().first.return_value = self.mock_contacts[0]
        updated_contact = await update_contact_fields(
            contact_id=1, body=contact_data, user=self.user, db=self.session
        )
        self.assertEqual(updated_contact.name, "John1")
        self.assertEqual(updated_contact.surname, "Doe1")
        self.assertEqual(updated_contact.email, "john1@example.com")
        self.assertEqual(updated_contact.phone_number, "123451")

    async def test_update_contact_fields_None(self):
        contact_data = ContactUpdateFields(
            name="John1", surname="Doe1", email="john1@example.com",
            phone_number="123451"
        )
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException):
            await update_contact_fields(
                contact_id=1, body=contact_data,
                user=self.user, db=self.session
            )

    async def test_delete_contact(self):
        self.session.query().filter().first.return_value = self.mock_contacts[0]
        res = await delete_contact(
            contact_id=1, user=self.user, db=self.session
        )
        self.assertIsNone(res)

    async def test_delete_contact_None(self):
        self.session.query().filter().first.return_value = None
        with self.assertRaises(HTTPException):
            res = await delete_contact(
                contact_id=1, user=self.user, db=self.session
            )

    async def test_get_birthdays(self):
        self.session.query().filter().all.return_value = self.mock_contacts
        birthdays = await get_birthdays(user=self.user, db=self.session)
        self.assertEqual(len(birthdays), 1)
        self.assertEqual(birthdays[0], self.mock_contacts[0])

if __name__ == '__main__':
    unittest.main()
