"""Patient router for FHIR-compliant patient endpoints."""

from typing import Optional

from fastapi import APIRouter, Query, Depends
from fhir.resources.bundle import Bundle
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.patient_service import search_patients, get_patient_by_guid

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get(
    "",
    summary="Search patients",
    description="""
    Search for patients using a single search parameter.
    
    The search term is matched against:
    - PESEL (Polish national identification number)
    - First name (case-insensitive)
    - Last name (case-insensitive)
    
    Returns a FHIR Bundle containing matching Patient resources.
    
    If no search parameter is provided, returns all patients.
    """,
    response_description="FHIR Bundle containing Patient resources",
)
async def get_patients(
    search: Optional[str] = Query(
        None,
        description="Search term to match against PESEL, first name, or last name",
        examples=["Jan", "Kowalski", "90010112345"],
    ),
    db: Session = Depends(get_db),
):
    bundle: Bundle = search_patients(db, search_term=search)
    return bundle.dict(exclude_none=True, by_alias=True)


@router.get(
    "/{guid}",
    summary="Get patient by GUID",
    description="""
    Retrieve a single patient by their internal GUID.
    
    Returns a FHIR Patient resource.
    """,
    response_description="FHIR Patient resource",
)
async def get_patient(
    guid: str,
    db: Session = Depends(get_db),
):
    patient = get_patient_by_guid(db, guid)
    return patient.dict(exclude_none=True, by_alias=True)
