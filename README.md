# LarvixON Patients Service

A FastAPI service providing mocked patient data using Fast Healthcare Interoperability Resources (FHIR) standards.

## Development

With the default port of '8001'

```sh
python -m uvicorn app.main:app --reload --port 8001
```

### Database commands

#### Seed database

X is the number of patients to create (if not specified, defaults to 50)

```sh
python -m app.database.commands.seed <X>
```

#### Clear database

```sh
python -m app.database.commands.clear
```

#### Print first X patients

X is the number of patients to print

```sh
python -m app.database.commands.print_x_first_patients <X>
```
