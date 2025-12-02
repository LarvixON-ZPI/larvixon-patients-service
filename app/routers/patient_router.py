import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Header
from fhir.resources.bundle import Bundle
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.requests.patients_guids_request import PatientGuidsRequest
from app.services.patient_service import (
    search_patients,
    get_patient_by_guid,
    get_patients_by_guids,
)

load_dotenv()
valid_tokens: list[str] = os.getenv("API_TOKENS", "").split(";")


def verify_token(x_api_token=Header(None)) -> None:
    if x_api_token not in valid_tokens:
        raise HTTPException(401, "Invalid API token")


router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    dependencies=[Depends(verify_token)],
)


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
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    pesel: Optional[str] = None,
    db: Session = Depends(get_db),
):
    bundle: Bundle = search_patients(db, first_name, last_name, pesel)
    return bundle.dict(exclude_none=True, by_alias=True)


@router.post(
    "/patients-by-guids",
    summary="Get patients by GUIDs",
    description="""
    Retrieve multiple patients by their internal GUIDs.
    
    Returns a FHIR Bundle containing Patient resources for all found GUIDs.
    Patients that don't exist are silently excluded from the results.
    """,
    response_description="FHIR Bundle containing Patient resources",
)
async def get_patients_by_guid_list(
    request: PatientGuidsRequest,
    db: Session = Depends(get_db),
):
    bundle: Bundle = get_patients_by_guids(db, request.guids)
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
