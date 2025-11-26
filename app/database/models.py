from typing import Any

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base: Any = declarative_base()


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pesel = Column(String(11), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=False, index=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address_line = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(2), default="PL")

    def to_dict(self) -> dict:
        return {
            "id": f"patient-{self.id:03d}",
            "pesel": self.pesel,
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
