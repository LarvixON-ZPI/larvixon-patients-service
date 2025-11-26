"""FHIR Patient resource utilities."""

from typing import Any, cast

from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.address import Address
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.fhirtypes import (
    Code,
    Uri,
    IdentifierType,
    HumanNameType,
    Date,
    ContactPointType,
    AddressType,
)


def create_fhir_patient(patient_data: dict[str, Any]) -> Patient:
    identifiers: list[Identifier] = [
        Identifier(  # type: ignore[call-arg]
            system=Uri("http://hl7.org/fhir/sid/pesel"),
            value=patient_data["pesel"],
            use=Code("official"),
        )
    ]

    names: list[HumanName] = [
        HumanName(  # type: ignore[call-arg]
            use=Code("official"),
            family=patient_data["last_name"],
            given=[patient_data["first_name"]],
        )
    ]

    telecoms: list[ContactPoint] = []
    if patient_data.get("phone"):
        telecoms.append(
            ContactPoint(  # type: ignore[call-arg]
                system=Code("phone"),
                value=patient_data["phone"],
                use=Code("mobile"),
            )
        )
    if patient_data.get("email"):
        telecoms.append(
            ContactPoint(  # type: ignore[call-arg]
                system=Code("email"),
                value=patient_data["email"],
                use=Code("home"),
            )
        )

    addresses: list[Address] = []
    if patient_data.get("address"):
        addr_data = patient_data["address"]
        addresses.append(
            Address(  # type: ignore[call-arg]
                use=Code("home"),
                line=addr_data.get("line", []),
                city=addr_data.get("city"),
                postalCode=addr_data.get("postal_code"),
                country=addr_data.get("country"),
            )
        )

    patient = Patient(  # type: ignore[call-arg]
        id=patient_data["id"],
        identifier=cast(list[IdentifierType], identifiers),
        name=cast(list[HumanNameType], names),
        gender=Code(patient_data.get("gender")),
        birthDate=cast(Date, patient_data.get("birth_date")),
        telecom=cast(list[ContactPointType], telecoms),
        address=cast(list[AddressType], addresses),
    )

    return patient
