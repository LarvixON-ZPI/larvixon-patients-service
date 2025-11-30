from typing import List

from pydantic import BaseModel


class PatientGuidsRequest(BaseModel):
    guids: List[str]
