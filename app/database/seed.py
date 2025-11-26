import random
from datetime import date, datetime
from typing import cast

from faker import Faker
from sqlalchemy.orm import Session

from .models import Patient
from .connection import SessionLocal, init_db

from logging import info, error

fake = Faker("pl_PL")


def create_fake_patient() -> dict:
    gender = random.choice(["male", "female"])

    if gender == "male":
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
    else:
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()

    birth_date = fake.date_of_birth(minimum_age=1, maximum_age=100)

    return {
        "pesel": fake.pesel(cast(datetime, birth_date), gender),
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


def seed_database(num_patients: int = 50) -> int:
    init_db()

    db: Session = SessionLocal()
    created_count = 0

    try:
        used_pesels: set[str] = set()

        for _ in range(num_patients):
            patient_data = create_fake_patient()

            retries = 0
            MAX_RETRIES = 100
            while patient_data["pesel"] in used_pesels:
                if retries >= MAX_RETRIES:
                    raise RuntimeError(
                        f"Could not generate a unique PESEL after {MAX_RETRIES} attempts."
                    )
                patient_data = create_fake_patient()
                retries += 1

            used_pesels.add(patient_data["pesel"])

            patient = Patient(**patient_data)
            db.add(patient)
            created_count += 1

        db.commit()
        info(f"Successfully created {created_count} patients.")

    except Exception as e:
        db.rollback()
        error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

    return created_count


if __name__ == "__main__":
    seed_database(50)
