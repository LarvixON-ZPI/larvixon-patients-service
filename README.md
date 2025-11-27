# LarvixON Patients Service

A FastAPI service providing mocked patient data using Fast Healthcare Interoperability Resources (FHIR) standards.

## Development

With the default port of '8001'

```sh
python -m uvicorn app.main:app --reload --port 8001
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
