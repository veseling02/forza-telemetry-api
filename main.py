from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import schemas
import models

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sessions", status_code=201)
def create_session(session: schemas.TelemetrySession, db: Session = Depends(get_db)) -> schemas.TelemetrySessionRead:
    row = models.TelemetrySession(
        started_at=session.started_at,
        max_rpm=session.max_rpm,
        samples=[models.TelemetrySample(**s.model_dump()) for s in session.samples]
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row