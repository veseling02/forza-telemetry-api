# Forza Telemetry API

![CI](https://github.com/veseling02/forza-telemetry-api/actions/workflows/ci.yml/badge.svg)

**Work in progress.**

A FastAPI backend for [Forza Live Telemetry](https://github.com/veseling02/forza-telemetry). The desktop app will send recorded driving sessions here to be stored and served back.

**Stack:** FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic, pytest, Docker, GitHub Actions.

It's a separate repo so the desktop app's pygame dependency stays out of the server and its CI.

## Status

Done:

- `GET /health`
- `POST /sessions`: validates a session and stores it in PostgreSQL
- `GET /sessions/{id}`: returns a stored session with its samples
- SQLAlchemy models and Alembic migrations
- Tests against a real PostgreSQL database, locally and in CI
- Docker image for the API, and Docker Compose running the API and PostgreSQL together

Next:

- JWT auth
- Deployment

## Example

A session is a start time, the car's maximum RPM, and a list of samples. Each sample is one telemetry packet: time since the start in milliseconds, pedal inputs from 0 to 1, steering from -1 to 1, speed and RPM.

`POST /sessions`

```json
{
  "started_at": "2026-09-25T21:14:00Z",
  "max_rpm": 8000.0,
  "samples": [
    {"t_ms": 0, "gas": 0.82, "brake": 0.0, "steer": -0.12, "speed_kmh": 143.6, "rpm": 6120.4}
  ]
}
```

Response, `201 Created`:

```json
{"id": 1, "started_at": "2026-09-25T21:14:00Z", "max_rpm": 8000.0}
```

`GET /sessions/1` returns the same session with its samples. Out-of-range values, such as `"gas": 1.5`, are rejected with a `422` that points at the exact sample and field.

## Run with Docker

Requires Docker.

1. Copy `.env.example` to `.env` (`cp .env.example .env`, or `copy .env.example .env` on Windows) and set `POSTGRES_PASSWORD` to a password of your choice. `.env` is ignored by git.
2. Start everything:

```bash
docker compose up --build
```

This builds the API image, starts PostgreSQL, waits until it's ready, applies the database migrations, and starts the API. The API is at http://127.0.0.1:8000, and the interactive docs are at http://127.0.0.1:8000/docs.

Press Ctrl+C once to stop. To run it in the background instead, use `docker compose up --build -d` and stop it with `docker compose down`. The data is kept in a Docker volume between runs; `docker compose down -v` deletes it.

## Development

For working on the code, run the API directly with auto-reload, against a PostgreSQL container. Requires Python 3.14 and Docker.

**1. Start PostgreSQL** in a container. Pick a password; you'll use it again in step 3.

```bash
docker run --name forza-pg -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=telemetry -p 5432:5432 -v forza-pgdata:/var/lib/postgresql/data -d postgres:17
```

After a reboot, start it again with `docker start forza-pg`.

**2. Create a virtual environment, activate it, and install the dependencies:**

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` on Windows, or `source .venv/bin/activate` on macOS and Linux. Your prompt should now start with `(.venv)`. Then:

```bash
pip install -r requirements-dev.txt
```

**3. Configure.** Copy `.env.example` to `.env` if you haven't already, and replace `CHANGE_ME` in `DATABASE_URL` and `TEST_DATABASE_URL` with your password from step 1.

**4. Create the tables:**

```bash
alembic upgrade head
```

**5. Run the API:**

```bash
uvicorn main:app --reload
```

Both this and the Docker setup use port 8000, so stop one before starting the other.

## Tests

The tests use a separate database in the development PostgreSQL container, so they never touch your data. Create it once:

```bash
docker exec forza-pg psql -U postgres -c "CREATE DATABASE telemetry_test;"
```

Then:

```bash
python -m pytest
```

Each test creates the tables it needs and drops them afterwards.
