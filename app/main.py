"""FastAPI application for Larvixon Patients Service."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.database.utils import check_if_has_patients
from app.routers import patient_router
from app.database import init_db
from app.database.seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    if not check_if_has_patients():
        seed_database(50)
    yield


app = FastAPI(
    title="Larvixon Patients Service",
    description="""
    A FHIR-compliant patient service API.
    
    This service provides endpoints for searching and retrieving patient data
    using the HL7 FHIR (Fast Healthcare Interoperability Resources) standard.
    
    ## Features
    
    - Search patients by PESEL, first name, or last name
    - FHIR R4 compliant Patient resources
    - Returns FHIR Bundle for search results
    """,
    version="1.0.0",
    contact={
        "name": "LarvixON",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

app.include_router(patient_router, prefix="/api/v1")


@app.get("/")
async def root():
    # redirect to API docs
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
