# LarvixON Patients Service

A FastAPI service providing mocked patient data using Fast Healthcare Interoperability Resources (FHIR) standards.

## Development

```sh
python -m uvicorn app.main:app --reload
```

### Database commands

Seed database

```sh
python -m app.database.commands.seed
```

Clear database

```sh
python -m app.database.commands.clear
```
