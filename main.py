from sqlalchemy.exc import IntegrityError
from security import hasher
from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import schemas
import models

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    row = models.User(username=user.username, password_hash=hasher.hash(user.password))
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username is already taken!")
    db.refresh(row)
    return row

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

@app.get("/sessions/{session_id}")
def read_session(session_id: int, db: Session = Depends(get_db)) -> schemas.TelemetrySessionDetail:
    row = db.get(models.TelemetrySession, session_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return row