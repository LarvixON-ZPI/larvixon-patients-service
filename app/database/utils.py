from app.database.connection import get_db
from app.database.models import Patient


def check_if_has_patients() -> bool:
    db = get_db()
    session = next(db)
    try:
        patient_count: int = session.query(Patient).count()
    finally:
        session.close()
    return patient_count > 0
