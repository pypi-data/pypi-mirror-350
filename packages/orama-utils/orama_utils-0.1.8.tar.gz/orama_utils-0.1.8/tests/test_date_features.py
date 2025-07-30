"""
Tests for date features module.
"""

import pandas as pd
import pytest
from orama_utils.date_features import add_date_features


@pytest.fixture
def sample_df():
    """Create a sample DataFrame with dates for testing."""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    return pd.DataFrame({'date': dates})


def test_add_date_features_basic(sample_df):
    """Test basic date feature extraction."""
    result = add_date_features(sample_df, date_column='date')
    
    # Check if all expected columns are present
    expected_columns = [
        'date_year', 'date_month', 'date_day', 'date_week_of_month',
        'date_week_of_year', 'date_quarter', 'date_is_monday',
        'date_is_tuesday', 'date_is_wednesday', 'date_is_thursday',
        'date_is_friday', 'date_is_saturday', 'date_is_sunday',
        'date_is_weekend', 'date_is_month_start', 'date_is_month_end',
        'date_is_quarter_start', 'date_is_quarter_end',
        'date_is_year_start', 'date_is_year_end', 'date_season'
    ]
    
    for col in expected_columns:
        assert col in result.columns


def test_add_date_features_specific_features(sample_df):
    """Test adding specific date features."""
    features = ['year', 'month', 'week_of_month', 'is_monday']
    result = add_date_features(sample_df, date_column='date', features=features)
    
    # Check if only specified columns are present
    expected_columns = ['date_year', 'date_month', 'date_week_of_month', 'date_is_monday']
    assert all(col in result.columns for col in expected_columns)
    assert len(result.columns) == len(expected_columns) + 1  # +1 for original date column


def test_add_date_features_week_of_month(sample_df):
    """Test week of month calculation."""
    result = add_date_features(sample_df, date_column='date', features=['week_of_month'])
    
    # Check first week of January 2024
    jan_first_week = result[result['date'].dt.month == 1]['date_week_of_month'].iloc[0]
    assert jan_first_week == 1
    
    # Check last week of January 2024
    jan_last_week = result[result['date'].dt.month == 1]['date_week_of_month'].iloc[-1]
    assert jan_last_week == 5


def test_add_date_features_day_flags(sample_df):
    """Test day of week flags."""
    result = add_date_features(sample_df, date_column='date', 
                             features=['is_monday', 'is_tuesday', 'is_wednesday', 
                                     'is_thursday', 'is_friday', 'is_saturday', 
                                     'is_sunday', 'is_weekend'])
    
    # Check January 1, 2024 (Monday)
    jan_first = result[result['date'] == '2024-01-01'].iloc[0]
    assert jan_first['date_is_monday'] == 1
    assert jan_first['date_is_weekend'] == 0
    
    # Check January 6, 2024 (Saturday)
    jan_sixth = result[result['date'] == '2024-01-06'].iloc[0]
    assert jan_sixth['date_is_saturday'] == 1
    assert jan_sixth['date_is_weekend'] == 1


def test_add_date_features_season(sample_df):
    """Test season calculation."""
    result = add_date_features(sample_df, date_column='date', features=['season'])
    
    # Check seasons for specific dates
    winter_date = result[result['date'] == '2024-01-15'].iloc[0]
    spring_date = result[result['date'] == '2024-04-15'].iloc[0]
    summer_date = result[result['date'] == '2024-07-15'].iloc[0]
    fall_date = result[result['date'] == '2024-10-15'].iloc[0]
    
    # Assert season values (1=Winter, 2=Spring, 3=Summer, 4=Fall)
    assert winter_date['date_season'] == 1
    assert spring_date['date_season'] == 2
    assert summer_date['date_season'] == 3
    assert fall_date['date_season'] == 4


def test_add_date_features_invalid_column():
    """Test handling of invalid date column."""
    df = pd.DataFrame({'not_date': [1, 2, 3]})
    with pytest.raises(ValueError):
        add_date_features(df, date_column='date')


def test_add_date_features_invalid_features(sample_df):
    """Test handling of invalid features."""
    with pytest.raises(ValueError):
        add_date_features(sample_df, date_column='date', features=['invalid_feature'])


def test_add_date_features_inplace(sample_df):
    """Test inplace modification."""
    original_df = sample_df.copy()
    result = add_date_features(sample_df, date_column='date', inplace=True)
    
    assert result is None
    assert 'date_year' in sample_df.columns
    assert len(sample_df.columns) > len(original_df.columns) 