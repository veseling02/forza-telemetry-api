from schemas import TelemetrySample
from pydantic import ValidationError
import pytest

VALID = {"t_ms": 17, "gas": 0.82, "brake": 0.0, "steer": -0.5, "rpm": 6340.4, "speed_kmh": 59.6}

def test_valid_sample():
    sample = TelemetrySample(**VALID)
    assert sample.gas == 0.82
    
@pytest.mark.parametrize("field, value", [
    ("gas", -0.01),
    ("gas", 1.01),
    ("brake", -0.01),
    ("brake", 1.01),
    ("steer", -1.01),
    ("steer", 1.01),
    ("speed_kmh", -0.01),
    ("rpm", -0.01),
    ("t_ms", -1),
])    
def test_out_of_range_data(field, value):
    data = VALID | {field: value}
    with pytest.raises(ValidationError):
        TelemetrySample(**data)
        
        
@pytest.mark.parametrize("field, value", [
    ("gas", 0.0),
    ("gas", 1.0),
    ("brake", 0.0),
    ("brake", 1.0),
    ("steer", -1.0),
    ("steer", 1.0),
    ("speed_kmh", 0.0),
    ("rpm", 0.0),
    ("t_ms", 0)
])
def test_in_range_data(field, value):
    data = VALID | {field: value}
    sample = TelemetrySample(**data)
    assert getattr(sample, field) == value