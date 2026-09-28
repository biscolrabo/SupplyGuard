# SupplyGuard

> Personal portfolio project inspired by incoming quality management in a manufacturing plant.

SupplyGuard is a web application to register, analyze, resolve and measure incidents caused by defective parts received from suppliers.

Incident workflow: `open → under analysis → corrective action → closed`.

## Tech stack

- **Backend:** FastAPI, Pydantic, SQLAlchemy 2.0, Alembic
- **Database:** PostgreSQL
- **Infrastructure:** Docker Compose

## Getting started

Requirements: Docker and Docker Compose.

```bash
cp .env.example .env   # then edit the values
docker compose up --build
```

## Project status

Work in progress — currently in **Phase 0** (project skeleton).
