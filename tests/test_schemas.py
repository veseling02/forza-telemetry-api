from schemas import TelemetrySample
from pydantic import ValidationError
import pytest

VALID = {"t_ms": 17, "gas": 0.82, "brake": 0.0, "steer": -0.5, "rpm": 6340.4, "speed_kmh": 59.6}

def test_valid_sample():
    sample = TelemetrySample(**VALID)
    assert sample.gas == 0.82
    
def test_invalid_gas():
    data = VALID | {"gas": 1.1}
    with pytest.raises(ValidationError):
        TelemetrySample(**data)