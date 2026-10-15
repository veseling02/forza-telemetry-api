from pydantic import BaseModel, Field, AwareDatetime, ConfigDict

class TelemetrySample(BaseModel):
    gas: float = Field(ge=0.0, le=1.0)
    brake: float = Field(ge=0.0, le=1.0)
    steer: float = Field(ge=-1.0, le=1.0)
    speed_kmh: float = Field(ge=0)
    rpm: float = Field(ge=0)
    t_ms: int = Field(ge=0) 
    model_config = ConfigDict(from_attributes=True)

class TelemetrySession(BaseModel):
    started_at: AwareDatetime
    max_rpm: float = Field(gt=0)
    samples: list[TelemetrySample] = Field(min_length=1)
    
class TelemetrySessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    started_at: AwareDatetime
    max_rpm: float = Field(gt=0)
    
class TelemetrySessionDetail(TelemetrySessionRead):
    samples: list[TelemetrySample]