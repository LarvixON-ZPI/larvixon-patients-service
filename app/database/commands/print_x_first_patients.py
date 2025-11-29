import logging
import sys
from pprint import pprint
from app.database.connection import get_db
from app.database.models import Patient
from logging import getLogger

logger = getLogger(__name__)


def print_first_patients(x: int):
    with next(get_db()) as session:
        patients = session.query(Patient).limit(x).all()
        for patient in patients:
            row = {c.name: getattr(patient, c.name) for c in patient.__table__.columns}
            logger.info(f"{row}\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m app.database.commands.print_x_first_patients <x>")
        sys.exit(1)
    try:
        x = int(sys.argv[1])
    except ValueError:
        print("x must be an integer.")
        sys.exit(1)
    print_first_patients(x)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
