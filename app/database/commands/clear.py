import logging
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, init_db
from app.database.models import Patient

logger: logging.Logger = logging.getLogger(__name__)


def clear_db() -> None:
    init_db()

    db: Session = SessionLocal()

    try:
        num_deleted = db.query(Patient).delete()
        db.commit()
        logger.info(f"Successfully deleted {num_deleted} patients from the database.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error clearing database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    clear_db()
