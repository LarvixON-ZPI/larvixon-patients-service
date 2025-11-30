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
from fastapi import HTTPException

from app.database import Patient
from app.fhir_utils import create_fhir_patient
import logging

logger = logging.getLogger(__name__)

ROWS_LIMIT = 100


def search_patients(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    pesel: Optional[str] = None,
) -> Bundle:
    query: Query[Patient] = db.query(Patient)

    filters = []
    if first_name:
        filters.append(Patient.first_name.ilike(f"%{first_name}%"))
    if last_name:
        filters.append(Patient.last_name.ilike(f"%{last_name}%"))
    if pesel:
        filters.append(Patient.pesel.like(f"%{pesel}%"))

    if filters:
        query = query.filter(or_(*filters))

    query = query.limit(ROWS_LIMIT)

    patients: List[Patient] = query.all()

    fhir_patients: List[FHIRPatient] = [
        create_fhir_patient(p.to_dict()) for p in patients
    ]

    bundle: Bundle = _create_search_bundle(fhir_patients)

    return bundle


def get_patient_by_guid(db: Session, guid: str) -> FHIRPatient:
    patient: Optional[Patient] = (
        db.query(Patient).filter(Patient.internal_guid == guid).first()
    )

    if not patient:
        raise HTTPException(
            status_code=404, detail=f"Patient with GUID {guid} not found"
        )

    fhir_patient: FHIRPatient = create_fhir_patient(patient.to_dict())
    return fhir_patient


def get_patients_by_guids(db: Session, guids: List[str]) -> Bundle:
    patients: List[Patient] = (
        db.query(Patient)
        .filter(Patient.internal_guid.in_(guids))
        .limit(ROWS_LIMIT)
        .all()
    )

    patients_not_found = set(guids) - {str(p.internal_guid) for p in patients}

    if patients_not_found:
        logger.warning(f"Patients not found for GUIDs: {patients_not_found}")

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
