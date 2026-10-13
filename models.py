from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class TelemetrySession(Base):
    __tablename__ = "telemetry_sessions"
    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    max_rpm: Mapped[float]
    samples: Mapped[list["TelemetrySample"]] = relationship(back_populates='session', cascade="all, delete-orphan")

class TelemetrySample(Base):
    __tablename__ = "telemetry_samples"
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("telemetry_sessions.id"))
    t_ms: Mapped[int]
    gas: Mapped[float]
    brake: Mapped[float]
    steer: Mapped[float]
    speed_kmh: Mapped[float]
    rpm: Mapped[float]
    session: Mapped[TelemetrySession] = relationship(back_populates="samples")
