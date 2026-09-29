# SupplyGuard

> Personal portfolio project inspired by incoming quality management in a manufacturing plant.

SupplyGuard is a web application to register, analyze, resolve and measure incidents caused by defective parts received from suppliers.

Incident workflow: `open → under analysis → corrective action → closed`.

## Tech stack

- **Backend:** FastAPI, Pydantic, SQLAlchemy 2.0, Alembic
- **Database:** PostgreSQL (hosted on [Neon](https://neon.tech))

## Getting started

Requirements: Python 3.13+ and a PostgreSQL database (e.g. a free [Neon](https://neon.tech) project).

```bash
cp .env.example .env          # then set DATABASE_URL to your connection string
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload # API docs at http://localhost:8000/docs
```

## Project status

Work in progress — currently in **Phase 0** (project skeleton).
