import pytest
import os
import pandas as pd
from water_properties import get_water_property

# Create sample data file for tests
@pytest.fixture(scope="module")
def sample_csv(tmp_path_factory):
    data = {
        't (°C)': [0, 50, 100],
        'pp (bar)': [0.0061, 0.1235, 1.013],
        'ρ (kg/dm³)': [0.9998, 0.988, 0.9584]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path_factory.mktemp("data") / "water_data.csv"
    df.to_csv(file_path, index=False)
    return str(file_path)

def test_valid_interpolation(sample_csv):
    density, vapour_pressure = get_water_property(25, sample_csv)
    # Expected density and pressure are interpolated between 0 and 50 °C
    assert 980 < density < 999  # check density reasonable range
    assert 0.05 < vapour_pressure < 0.12  # check vapour pressure reasonable range

def test_temp_below_range(sample_csv):
    with pytest.raises(ValueError):
        get_water_property(-10, sample_csv)

def test_temp_above_range(sample_csv):
    with pytest.raises(ValueError):
        get_water_property(400, sample_csv)

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_water_property(25, "non_existent_file.csv")

def test_missing_column(tmp_path_factory):
    # Create a CSV missing the 'pp (bar)' column
    data = {
        't (°C)': [0, 50, 100],
        'ρ (kg/dm³)': [0.9998, 0.988, 0.9584]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path_factory.mktemp("data") / "bad_data.csv"
    df.to_csv(file_path, index=False)
    with pytest.raises(KeyError):
        get_water_property(25, str(file_path))

def test_unsupported_file_format(tmp_path_factory):
    file_path = tmp_path_factory.mktemp("data") / "data.txt"
    with open(file_path, 'w') as f:
        f.write("dummy text")
    with pytest.raises(ValueError):
        get_water_property(25, str(file_path))
