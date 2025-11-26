from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.patient import Patient as FHIRPatient

from app.database import Patient
from app.fhir_utils import create_fhir_patient


def search_patients(db: Session, search_term: Optional[str] = None) -> Bundle:
    query = db.query(Patient)

    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.filter(
            or_(
                Patient.pesel.like(search_pattern),
                Patient.first_name.ilike(search_pattern),
                Patient.last_name.ilike(search_pattern),
            )
        )

    patients = query.all()

    fhir_patients = [create_fhir_patient(p.to_dict()) for p in patients]

    bundle = _create_search_bundle(fhir_patients)

    return bundle


def _create_search_bundle(patients: list[FHIRPatient]) -> Bundle:
    entries: List[BundleEntry] = []
    for patient in patients:
        entry = BundleEntry(  # type: ignore[call-arg, arg-type]
            resource=patient, full_url=f"urn:uuid:{patient.id}"  # type: ignore[arg-type]
        )
        entries.append(entry)

    assert entries is not None

    bundle = Bundle(  # type: ignore[call-arg, arg-type]
        type="searchset", total=len(patients), entry=entries  # type: ignore[arg-type]
    )

    return bundle
