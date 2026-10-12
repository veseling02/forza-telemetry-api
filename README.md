# Forza Telemetry API

![CI](https://github.com/veseling02/forza-telemetry-api/actions/workflows/ci.yml/badge.svg)

**Work in progress.**

A FastAPI backend for [Forza Live Telemetry](https://github.com/veseling02/forza-telemetry). The desktop app will send recorded driving sessions here to be stored and served back.

It's a separate repo so the desktop app's pygame dependency stays out of the server and its CI.

## Status

Done:

- `GET /health`
- Tests and CI

Next:

- `POST /sessions`
- PostgreSQL with SQLAlchemy and Alembic
- JWT auth
- Docker Compose
- Deployment

## Run locally

Requires Python 3.14.

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Tests

```bash
python -m pytest
```
