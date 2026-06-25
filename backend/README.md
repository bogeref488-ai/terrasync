# TerraSync Backend

FastAPI backend foundation for TerraSync.

## Features in this starter

- FastAPI application structure
- Health check endpoint
- Work orders endpoint
- Sites endpoint
- Inspection templates endpoint
- Reports endpoint
- Defects endpoint
- PostgreSQL-ready configuration
- SQLAlchemy database setup
- Pydantic schemas
- Docker support

## Run locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Environment variables

Copy `.env.example` to `.env`.

```bash
cp .env.example .env
```
