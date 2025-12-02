import logging
import sys
from typing import Any

from faker import Faker
from sqlalchemy.orm import Session

from ..models import Patient
from ..connection import SessionLocal, init_db

logger: logging.Logger = logging.getLogger(__name__)

fake = Faker("pl_PL")


def seed_database(num_patients: int = 50) -> int:
    init_db()

    db: Session = SessionLocal()
    created_count = 0

    try:
        used_pesels: set[str] = set()

        for _ in range(num_patients):
            patient_data: dict[str, Any] = Patient.create_fake_patient(fake)

            retries = 0
            max_retries = 100
            if patient_data["pesel"] is not None:
                while patient_data["pesel"] in used_pesels:
                    if retries >= max_retries:
                        raise RuntimeError(
                            f"Could not generate a unique PESEL after {max_retries} attempts."
                        )
                    patient_data = Patient.create_fake_patient(fake)
                    retries += 1

            used_pesels.add(patient_data["pesel"])

            patient = Patient(**patient_data)
            db.add(patient)
            created_count += 1

        db.commit()
        logger.info(f"Successfully created {created_count} patients.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise
    finally:
        db.close()

    return created_count


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m app.database.commands.print_x_first_patients <x>")
        sys.exit(1)
    try:
        x = int(sys.argv[1])
    except ValueError:
        print("x must be an integer.")
        sys.exit(1)
    seed_database(x)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
