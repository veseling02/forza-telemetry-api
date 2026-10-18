from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]

class TelemetrySession(Base):
    __tablename__ = "telemetry_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    max_rpm: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    samples: Mapped[list["TelemetrySample"]] = relationship(back_populates='session', cascade="all, delete-orphan", order_by="TelemetrySample.t_ms")

class TelemetrySample(Base):
    __tablename__ = "telemetry_samples"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("telemetry_sessions.id"), index=True)
    t_ms: Mapped[int]
    gas: Mapped[float]
    brake: Mapped[float]
    steer: Mapped[float]
    speed_kmh: Mapped[float]
    rpm: Mapped[float]
    session: Mapped[TelemetrySession] = relationship(back_populates="samples")
