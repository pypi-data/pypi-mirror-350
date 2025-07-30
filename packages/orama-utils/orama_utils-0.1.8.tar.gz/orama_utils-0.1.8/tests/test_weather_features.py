import pytest
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from orama_utils.weather_features import add_weather_features

@pytest.fixture
def sample_df():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2025-05-20', periods=5),
        'location': ['Barcelona, Spain'] * 5
    })

@pytest.fixture
def mock_weather_data():
    """Create mock weather data for testing."""
    return pd.DataFrame({
        'datetime': pd.date_range(start='2025-05-20', periods=5),
        'tempmax': [20, 21, 22, 23, 24],
        'tempmin': [15, 16, 17, 18, 19],
        'temp': [17.5, 18.5, 19.5, 20.5, 21.5],
        'feelslike': [16, 17, 18, 19, 20],
        'precip': [0, 0.1, 0, 0.2, 0],
        'snow': [0, 0, 0, 0, 0],
        'windspeed': [10, 11, 12, 13, 14],
        'cloudcover': [30, 40, 50, 60, 70]
    })

@pytest.fixture
def weather_db_path(tmp_path):
    """Create a temporary weather database directory."""
    return str(tmp_path / "weather_db")

def test_missing_required_columns():
    """Test that function raises ValueError when required columns are missing."""
    df = pd.DataFrame({'date': [datetime.now()]})
    with pytest.raises(ValueError, match=r"DataFrame must contain columns: \['date', 'location'\]"):
        add_weather_features(df, "dummy_api_key")

def test_historical_data_not_implemented():
    """Test that function raises NotImplementedError for historical data."""
    df = pd.DataFrame({
        'date': [datetime.now() - timedelta(days=1)],
        'location': ['Barcelona, Spain']
    })
    with pytest.raises(NotImplementedError, match="Historical weather data fetching not implemented yet"):
        add_weather_features(df, "dummy_api_key")

def test_invalid_api_key(sample_df, weather_db_path, monkeypatch):
    """Test that function raises ValueError for invalid API key."""
    def mock_urlopen(*args, **kwargs):
        raise Exception("Invalid API key")
    
    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)
    
    with pytest.raises(ValueError, match="Error fetching weather data for Barcelona, Spain"):
        add_weather_features(sample_df, "invalid_api_key", weather_db_path=weather_db_path)

# TODO: more tests are needed