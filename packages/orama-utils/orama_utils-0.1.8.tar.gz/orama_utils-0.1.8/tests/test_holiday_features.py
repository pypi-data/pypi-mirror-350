"""
Tests for the holiday features module.
"""

import pytest
import pandas as pd
from orama_utils.holiday_features import add_holiday_features

def test_add_holiday_features_basic():
    """Test basic functionality with Spanish holidays."""
    # Create test data
    df = pd.DataFrame({
        'date': ['2019-01-01', '2019-01-06', '2019-02-28'],
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-MD', 'ES-MD', 'ES-AN']
    })
    
    # Apply holiday features
    result = add_holiday_features(df)
    
    # Check results
    assert result['is_public_holiday'].tolist() == [True, True, False]
    assert result['is_local_holiday'].tolist() == [False, False, True]
    assert result['many_counties_holiday'].tolist() == [False, False, False]

def test_add_holiday_features_italy():
    """Test handling of Italian holidays (currently empty)."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['IT'],
        'county': ['IT-25']
    })
    
    result = add_holiday_features(df)
    assert not result['is_public_holiday'].iloc[0]
    assert not result['is_local_holiday'].iloc[0]
    assert not result['many_counties_holiday'].iloc[0]

def test_add_holiday_features_mixed_countries():
    """Test handling of mixed country codes."""
    df = pd.DataFrame({
        'date': ['2019-01-01', '2019-01-01'],
        'country': ['ES', 'IT'],
        'county': ['ES-MD', 'IT-25']
    })
    
    result = add_holiday_features(df)
    assert result['is_public_holiday'].tolist() == [True, False]

def test_add_holiday_features_invalid_country():
    """Test error handling for invalid country codes."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['FR'],  # Invalid country code
        'county': ['FR-01']
    })
    
    with pytest.raises(ValueError, match=r"Invalid country codes found:.*"):
        add_holiday_features(df)

def test_add_holiday_features_missing_columns():
    """Test error handling for missing required columns."""
    # Missing date column
    df1 = pd.DataFrame({
        'country': ['ES'],
        'county': ['ES-MD']
    })
    with pytest.raises(ValueError, match=r"Date column.*not found"):
        add_holiday_features(df1)
    
    # Missing country column
    df2 = pd.DataFrame({
        'date': ['2019-01-01'],
        'county': ['ES-MD']
    })
    with pytest.raises(ValueError, match=r"Country column.*not found"):
        add_holiday_features(df2)

def test_add_holiday_features_custom_column_names():
    """Test using custom column names."""
    df = pd.DataFrame({
        'fecha': ['2019-01-01'],
        'pais': ['ES'],
        'region': ['ES-MD']
    })
    
    result = add_holiday_features(
        df,
        date_column='fecha',
        country_column='pais',
        county_column='region'
    )
    assert result['is_public_holiday'].iloc[0]

def test_add_holiday_features_county_threshold():
    """Test the county threshold functionality."""
    df = pd.DataFrame({
        'date': ['2019-04-18'],  # Maundy Thursday - many regions
        'country': ['ES'],
        'county': ['ES-MD']
    })
    
    # Test with default threshold (3)
    result1 = add_holiday_features(df)
    assert result1['many_counties_holiday'].iloc[0]
    
    # Test with higher threshold
    result2 = add_holiday_features(df, county_threshold=10)
    assert result2['many_counties_holiday'].iloc[0]
    
    # Test with very high threshold
    result3 = add_holiday_features(df, county_threshold=20)
    assert not result3['many_counties_holiday'].iloc[0]

def test_add_holiday_features_invalid_threshold():
    """Test error handling for invalid county threshold."""
    df = pd.DataFrame({
        'date': ['2019-01-01'],
        'country': ['ES'],
        'county': ['ES-MD']
    })
    
    with pytest.raises(ValueError, match="county_threshold must be a positive integer"):
        add_holiday_features(df, county_threshold=0)
    
    with pytest.raises(ValueError, match="county_threshold must be a positive integer"):
        add_holiday_features(df, county_threshold=-1)

def test_add_holiday_features_date_range():
    """Test date range validation."""
    # Test future dates
    future_df = pd.DataFrame({
        'date': ['2024-01-01', '2026-12-31'],
        'country': ['ES', 'ES'],
        'county': ['ES-MD', 'ES-MD']
    })
    
    with pytest.raises(ValueError) as exc_info:
        add_holiday_features(future_df)
    assert "is outside the available holiday data range" in str(exc_info.value)
    assert "keti@oramasolutions.io" in str(exc_info.value)
    
    # Test past dates
    past_df = pd.DataFrame({
        'date': ['2018-01-01', '2022-12-31'],
        'country': ['ES', 'ES'],
        'county': ['ES-MD', 'ES-MD']
    })
    
    with pytest.raises(ValueError) as exc_info:
        add_holiday_features(past_df)
    assert "is outside the available holiday data range" in str(exc_info.value)
    assert "keti@oramasolutions.io" in str(exc_info.value)

def test_day_before_public_holiday():
    """Test the day before public holiday feature."""
    # Create test data with day before and day of a public holiday
    df = pd.DataFrame({
        'date': ['2019-12-31', '2020-01-01', '2020-01-02'],  # Day before New Year, New Year, Day after
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-MD', 'ES-MD', 'ES-MD']
    })
    
    result = add_holiday_features(df)
    
    # New Year's day (Jan 1) is a public holiday
    assert result['is_public_holiday'].tolist() == [False, True, False]
    
    # Dec 31 should be marked as day before holiday
    assert result['is_day_before_holiday'].tolist() == [True, False, False]
    
    # Jan 2 should be marked as day after holiday
    assert result['is_day_after_holiday'].tolist() == [False, False, True]

def test_day_before_local_holiday():
    """Test the day before local holiday feature."""
    # Create test data with day before and day of a local holiday
    df = pd.DataFrame({
        'date': ['2019-02-27', '2019-02-28', '2019-03-01'],  # Around Day of Andalucía (Feb 28)
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-AN', 'ES-AN', 'ES-AN']  # This county celebrates this holiday
    })
    
    result = add_holiday_features(df)
    
    # Feb 28 is a local holiday for ES-AN
    assert result['is_local_holiday'].tolist() == [False, True, False]
    
    # Feb 27 should be marked as day before holiday
    assert result['is_day_before_holiday'].tolist() == [True, False, False]
    
    # Mar 1 should be marked as day after holiday
    assert result['is_day_after_holiday'].tolist() == [False, False, True]

def test_day_before_not_for_other_counties():
    """Test that day before/after flags don't apply to counties without the holiday."""
    # Create test data for different counties around a local holiday
    df = pd.DataFrame({
        'date': ['2019-02-27', '2019-02-28', '2019-03-01'],  # Around Day of Andalucía (Feb 28)
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-MD', 'ES-MD', 'ES-MD']  # Madrid doesn't celebrate Andalucía day
    })
    
    result = add_holiday_features(df)
    
    # Feb 28 is not a holiday for ES-MD
    assert not result['is_local_holiday'].iloc[1]
    assert not result['is_public_holiday'].iloc[1]
    
    # Neither Feb 27 nor Mar 1 should be marked as day before/after holiday
    assert not result['is_day_before_holiday'].iloc[0]
    assert not result['is_day_after_holiday'].iloc[2]

def test_day_before_after_works_with_gaps():
    """Test that day before/after flags work correctly with non-consecutive dates."""
    # Create test data with gaps around holidays
    df = pd.DataFrame({
        'date': ['2019-12-30', '2020-01-01', '2020-01-03'],  # Skip Dec 31 and Jan 2
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-MD', 'ES-MD', 'ES-MD']
    })
    
    result = add_holiday_features(df)
    
    # Jan 1 is a public holiday
    assert result['is_public_holiday'].tolist() == [False, True, False]
    
    # Dec 30 should not be marked as day before holiday (Dec 31 is missing)
    assert not result['is_day_before_holiday'].iloc[0]
    
    # Jan 3 should not be marked as day after holiday (Jan 2 is missing)
    assert not result['is_day_after_holiday'].iloc[2]

def test_day_before_many_counties_holiday():
    """Test that day before/after flags don't consider many_counties_holiday."""
    # Create test data around a holiday celebrated by many counties but not marked as public/local
    df = pd.DataFrame({
        'date': ['2019-04-17', '2019-04-18', '2019-04-19'],  # Around Maundy Thursday (Apr 18)
        'country': ['ES', 'ES', 'ES'],
        'county': ['ES-XX', 'ES-XX', 'ES-XX']  # Made-up county that doesn't celebrate this holiday
    })
    
    # Custom implementation to set many_counties_holiday but not public/local
    result = add_holiday_features(df)
    
    # Many counties celebrate Apr 18, but it's not a public holiday for ES-XX
    assert result['many_counties_holiday'].iloc[1]
    assert not result['is_public_holiday'].iloc[1]
    assert not result['is_local_holiday'].iloc[1]
    
    # Neither Apr 17 nor Apr 19 should be marked as day before/after holiday
    assert not result['is_day_before_holiday'].iloc[0]
    assert not result['is_day_after_holiday'].iloc[2]
    
    # Now let's check with a real county that celebrates it
    df['county'] = ['ES-MD', 'ES-MD', 'ES-MD']
    result = add_holiday_features(df)
    
    # Should be a local holiday for ES-MD
    assert result['is_local_holiday'].iloc[1]
    
    # Now Apr 17 and Apr 19 should be marked as day before/after
    assert result['is_day_before_holiday'].iloc[0]
    assert result['is_day_after_holiday'].iloc[2] 