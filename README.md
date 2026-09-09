# Forza Telemetry API

![CI](https://github.com/veseling02/forza-telemetry-api/actions/workflows/ci.yml/badge.svg)

A REST API for storing and serving racing telemetry sessions, built with FastAPI and PostgreSQL.

## About

This is the server half of [Forza Live Telemetry](https://github.com/veseling02/forza-telemetry), a desktop dashboard that catches Forza's UDP telemetry packets and draws them live at 60 fps. The dashboard is good at showing you what happened in the last four seconds and useless at showing you what happened last Tuesday — it keeps nothing. This API is where sessions go to be kept.

The desktop client will POST a finished session as JSON; this service validates it, stores it in Postgres against a user account, and serves it back. Every user sees only their own laps.

It's a separate repository on purpose. The dashboard needs pygame and a display, neither of which exists on a server, and I didn't want a GUI dependency sitting in this project's requirements or in its CI. The two talk over HTTP and share nothing else.

## Status

Early. Working now:

- [x] `GET /health`
- [x] Test suite with pytest
- [x] CI running the tests on every push

Planned:

- [ ] Session and user models with SQLAlchemy, migrations with Alembic
- [ ] PostgreSQL instead of nothing
- [ ] JWT auth, scoped so users only see their own sessions
- [ ] Docker Compose so the API and database come up in one command
- [ ] End-to-end tests with Playwright
- [ ] Deployed somewhere with a public URL

## Running locally

Requires Python 3.14.

```bash
git clone https://github.com/veseling02/forza-telemetry-api.git
cd forza-telemetry-api
python -m venv .venv
```

Activate the virtual environment — `.venv\Scripts\Activate.ps1` on Windows, `source .venv/bin/activate` on macOS and Linux. Then:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is at http://127.0.0.1:8000. Interactive docs, generated from the endpoint signatures, are at http://127.0.0.1:8000/docs.

## Tests

```bash
python -m pytest
```

The tests use FastAPI's `TestClient`, which calls the application directly rather than over a socket, so nothing needs to be running first.
