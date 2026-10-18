from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from security import hasher, create_access_token, DUMMY_HASH, get_current_user
from database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from config import settings
import schemas
import models

app = FastAPI()

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserRead:
    if not settings.allow_registration:
        raise HTTPException(status_code=403, detail="Registration is disabled")
    row = models.User(username=user.username, password_hash=hasher.hash(user.password))
    db.add(row)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username is already taken!")
    db.refresh(row)
    return row

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> schemas.Token:
    user = db.scalar(select(models.User).where(models.User.username == form.username))
    password_hash = user.password_hash if user else DUMMY_HASH
    password_ok = hasher.verify(form.password, password_hash)
    if user is None or not password_ok:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schemas.Token(access_token=create_access_token(user.id), token_type="bearer")

@app.get("/users/me")
def read_me(user: models.User = Depends(get_current_user)) -> schemas.UserRead:
    return user

@app.post("/sessions", status_code=201)
def create_session(session: schemas.TelemetrySession, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)) -> schemas.TelemetrySessionRead:
    row = models.TelemetrySession(
        user_id=user.id,
        started_at=session.started_at,
        max_rpm=session.max_rpm,
        samples=[models.TelemetrySample(**s.model_dump()) for s in session.samples]
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@app.get("/sessions/{session_id}")
def read_session(session_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)) -> schemas.TelemetrySessionDetail:
    row = db.get(models.TelemetrySession, session_id)
    if row is None or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    return row