from fastapi import FastAPI
from schemas import TelemetrySession

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sessions", status_code=201)
def create_session(session: TelemetrySession) -> TelemetrySession:
    return session