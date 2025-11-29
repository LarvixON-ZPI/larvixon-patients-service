from typing import List

from pydantic import BaseModel


class PatientGuidsRequest(BaseModel):
    """Request model for fetching patients by GUIDs."""

    guids: List[str]
