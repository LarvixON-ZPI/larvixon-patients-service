from typing import List, Optional, cast

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fhir.resources.bundle import Bundle, BundleEntry
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.fhirtypes import (
    ResourceType,
    Uri,
    Code,
    UnsignedInt,
    BundleEntryType,
)
from sqlalchemy.orm.query import Query

from app.database import Patient
from app.fhir_utils import create_fhir_patient


def search_patients(db: Session, search_term: Optional[str] = None) -> Bundle:
    query: Query[Patient] = db.query(Patient)

    if search_term:
        search_pattern: str = f"%{search_term}%"
        query = query.filter(
            or_(
                Patient.pesel.like(search_pattern),
                Patient.first_name.ilike(search_pattern),
                Patient.last_name.ilike(search_pattern),
            )
        )

    patients: List[Patient] = query.all()

    fhir_patients: List[FHIRPatient] = [
        create_fhir_patient(p.to_dict()) for p in patients
    ]

    bundle: Bundle = _create_search_bundle(fhir_patients)

    return bundle


def _create_search_bundle(patients: list[FHIRPatient]) -> Bundle:
    entries: List[BundleEntry] = []
    for patient in patients:
        entry = BundleEntry(  # type: ignore[call-arg]
            resource=cast(ResourceType, patient),
            fullUrl=Uri(f"urn:uuid:{patient.id}"),
        )
        entries.append(entry)

    assert entries is not None

    bundle = Bundle(  # type: ignore[call-arg]
        type=Code("searchset"),
        total=UnsignedInt(len(patients)),
        entry=cast(List[BundleEntryType], entries),
    )

    return bundle
