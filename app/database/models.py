from datetime import datetime
import random
from typing import Any, cast
import uuid

import faker
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base: Any = declarative_base()

NO_PESEL_PROBABILITY: float = 0.1


class Patient(Base):
    __tablename__ = "patients"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    internal_guid: Column[str] = Column(String, unique=True, nullable=False)
    pesel: Column[str] = Column(String(11), unique=True, nullable=True, index=True)
    first_name: Column[str] = Column(String(100), nullable=False, index=True)
    last_name: Column[str] = Column(String(100), nullable=False, index=True)
    birth_date = Column(Date, nullable=True)
    gender: Column[str] = Column(String(10), nullable=True)
    phone: Column[str] = Column(String(20), nullable=True)
    email: Column[str] = Column(String(255), nullable=True)
    address_line: Column[str] = Column(String(255), nullable=True)
    city: Column[str] = Column(String(100), nullable=True)
    postal_code: Column[str] = Column(String(10), nullable=True)
    country: Column[str] = Column(String(2), default="PL")

    def to_dict(self) -> dict:
        return {
            "id": f"patient-{self.id:03d}",
            "pesel": self.pesel,
            "internal_guid": self.internal_guid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": (
                self.birth_date.isoformat() if self.birth_date is not None else None
            ),
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": {
                "line": [self.address_line] if self.address_line is not None else [],
                "city": self.city,
                "postal_code": self.postal_code,
                "country": self.country,
            },
        }

    @staticmethod
    def create_fake_patient(fake: faker.Faker) -> dict[str, Any]:
        gender: str = random.choice(["male", "female"])

        first_name: str
        last_name: str
        if gender == "male":
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()

        birth_date = fake.date_of_birth(minimum_age=1, maximum_age=100)

        pesel: str | None = None
        if random.random() < NO_PESEL_PROBABILITY:
            pesel = fake.pesel(cast(datetime, birth_date), gender)

        return {
            "internal_guid": str(uuid.uuid4()),
            "pesel": pesel,
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "gender": gender,
            "phone": fake.phone_number(),
            "email": fake.email(),
            "address_line": fake.street_address(),
            "city": fake.city(),
            "postal_code": fake.postcode(),
            "country": "PL",
        }
