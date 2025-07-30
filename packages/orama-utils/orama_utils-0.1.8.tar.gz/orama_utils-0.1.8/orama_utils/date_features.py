"""
Date Features Module

This module provides functions to extract and add date-related features to pandas DataFrames.
"""

import pandas as pd
from typing import List, Optional, Union
import numpy as np


def add_date_features(
    df: pd.DataFrame,
    date_column: str = "date",
    features: Optional[List[str]] = None,
    inplace: bool = False,
) -> Optional[pd.DataFrame]:
    """
    Add date-related features to a pandas DataFrame based on a datetime column.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing a date column.
    date_column : str, default="date"
        Name of the column containing datetime values.
    features : list of str, optional
        List of features to add. If None, all available features will be added.
        Available features: 
        ['year', 'month', 'day', 'week_of_month', 'week_of_year', 
        'quarter', 'is_monday', 'is_tuesday', 'is_wednesday', 'is_thursday',
        'is_friday', 'is_saturday', 'is_sunday', 'is_weekend',
        'is_month_start', 'is_month_end', 'is_quarter_start', 
        'is_quarter_end', 'is_year_start', 'is_year_end', 'season']
    inplace : bool, default=False
        If True, add the features to the input DataFrame. If False, return a copy.
    
    Returns
    -------
    pd.DataFrame or None
        If inplace=False, returns DataFrame with added date features.
        If inplace=True, returns None.
        
    Raises
    ------
    ValueError
        If the date_column is not found in the DataFrame or is not of datetime dtype.
    """
    # Make a copy if not inplace
    if not inplace:
        df = df.copy()
    
    # Check if date column exists
    if date_column not in df.columns:
        raise ValueError(f"Column '{date_column}' not found in the DataFrame")
    
    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        try:
            df[date_column] = pd.to_datetime(df[date_column])
        except Exception as e:
            raise ValueError(f"Could not convert '{date_column}' to datetime: {str(e)}")
    
    # Define available features
    all_features = [
        'year', 'month', 'day', 'week_of_month', 'week_of_year', 
        'quarter', 'is_monday', 'is_tuesday', 'is_wednesday', 'is_thursday',
        'is_friday', 'is_saturday', 'is_sunday', 'is_weekend',
        'is_month_start', 'is_month_end', 'is_quarter_start', 
        'is_quarter_end', 'is_year_start', 'is_year_end', 'season'
    ]
    
    # Use provided features or default to all
    features_to_add = features if features is not None else all_features
    
    # Validate features
    invalid_features = [f for f in features_to_add if f not in all_features]
    if invalid_features:
        raise ValueError(f"Invalid features: {invalid_features}. Available features: {all_features}")
    
    # Extract date components
    date_series = df[date_column]
    
    # Basic date components
    if 'year' in features_to_add:
        df[f'{date_column}_year'] = date_series.dt.year
    
    if 'month' in features_to_add:
        df[f'{date_column}_month'] = date_series.dt.month
    
    if 'day' in features_to_add:
        df[f'{date_column}_day'] = date_series.dt.day
    
    if 'week_of_month' in features_to_add:
        # Calculate week of month (1-5)
        df[f'{date_column}_week_of_month'] = ((date_series.dt.day - 1) // 7) + 1
    
    if 'week_of_year' in features_to_add:
        df[f'{date_column}_week_of_year'] = date_series.dt.isocalendar().week
    
    if 'quarter' in features_to_add:
        df[f'{date_column}_quarter'] = date_series.dt.quarter
    
    # Day of week flags
    if 'is_monday' in features_to_add:
        df[f'{date_column}_is_monday'] = (date_series.dt.dayofweek == 0).astype(int)
    
    if 'is_tuesday' in features_to_add:
        df[f'{date_column}_is_tuesday'] = (date_series.dt.dayofweek == 1).astype(int)
    
    if 'is_wednesday' in features_to_add:
        df[f'{date_column}_is_wednesday'] = (date_series.dt.dayofweek == 2).astype(int)
    
    if 'is_thursday' in features_to_add:
        df[f'{date_column}_is_thursday'] = (date_series.dt.dayofweek == 3).astype(int)
    
    if 'is_friday' in features_to_add:
        df[f'{date_column}_is_friday'] = (date_series.dt.dayofweek == 4).astype(int)
    
    if 'is_saturday' in features_to_add:
        df[f'{date_column}_is_saturday'] = (date_series.dt.dayofweek == 5).astype(int)
    
    if 'is_sunday' in features_to_add:
        df[f'{date_column}_is_sunday'] = (date_series.dt.dayofweek == 6).astype(int)
    
    if 'is_weekend' in features_to_add:
        df[f'{date_column}_is_weekend'] = date_series.dt.dayofweek.isin([5, 6]).astype(int)
    
    # Boolean flags
    if 'is_month_start' in features_to_add:
        df[f'{date_column}_is_month_start'] = date_series.dt.is_month_start.astype(int)
    
    if 'is_month_end' in features_to_add:
        df[f'{date_column}_is_month_end'] = date_series.dt.is_month_end.astype(int)
    
    if 'is_quarter_start' in features_to_add:
        df[f'{date_column}_is_quarter_start'] = date_series.dt.is_quarter_start.astype(int)
    
    if 'is_quarter_end' in features_to_add:
        df[f'{date_column}_is_quarter_end'] = date_series.dt.is_quarter_end.astype(int)
    
    if 'is_year_start' in features_to_add:
        df[f'{date_column}_is_year_start'] = date_series.dt.is_year_start.astype(int)
    
    if 'is_year_end' in features_to_add:
        df[f'{date_column}_is_year_end'] = date_series.dt.is_year_end.astype(int)
    
    # Season (Northern Hemisphere)
    if 'season' in features_to_add:
        month = date_series.dt.month
        # Map seasons to integers: 1=Winter, 2=Spring, 3=Summer, 4=Fall
        df[f'{date_column}_season'] = pd.cut(
            month, 
            bins=[0, 3, 6, 9, 12], 
            labels=[1, 2, 3, 4],  # Integer labels
            include_lowest=False, 
            right=True
        ).astype(int)  # Convert to integer
    
    # Return None if inplace=True, otherwise return the DataFrame
    return None if inplace else df 