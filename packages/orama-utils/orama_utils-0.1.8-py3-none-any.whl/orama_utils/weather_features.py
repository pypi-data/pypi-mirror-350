import os
import json
import pandas as pd
import urllib.request
import urllib.parse
import csv
import codecs
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Union
import pathlib

# Set up logging
logger = logging.getLogger(__name__)

def add_weather_features(
    df: pd.DataFrame,
    api_key: str,
    features: Optional[List[str]] = None,
    weather_db_path: Optional[str] = None
) -> pd.DataFrame:
    """
    Add weather features to a dataframe based on date and location columns.
    
    Args:
        df (pd.DataFrame): Input dataframe with 'date' and 'location' columns
        api_key (str): Visual Crossing Weather API key (you can get it from https://www.visualcrossing.com/weather-api)
        features (List[str], optional): List of weather features to include. If None, includes all available features.
            Available features: ['datetime', 'tempmax', 'tempmin', 'temp', 'feelslike', 
                               'precip', 'snow', 'windspeed', 'cloudcover']
        weather_db_path (str, optional): Path to store weather data files. 
            If None, it will use the WEATHER_DB_PATH environment variable or default to /tmp/weather_db in Lambda,
            or ./weather_db in non-Lambda environments.
    
    Returns:
        pd.DataFrame: Original dataframe with added weather features
    Raises:
        ValueError: If the input dataframe is missing required columns or the API key is invalid
        NotImplementedError: If historical weather data fetching is not implemented
    """
    # Validate input dataframe
    required_columns = ['date', 'location']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain columns: {required_columns}")
    
    # Determine appropriate weather_db_path based on environment
    if weather_db_path is None:
        # Check environment variable first
        weather_db_path = os.environ.get('WEATHER_DB_PATH')
        
        # If not set in environment, check if we're in Lambda (check for standard Lambda env vars)
        if weather_db_path is None:
            if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
                # In Lambda, use /tmp
                weather_db_path = '/tmp/weather_db'
                logger.info("Running in AWS Lambda environment, using /tmp/weather_db")
            else:
                # Not in Lambda, use local directory
                weather_db_path = 'weather_db'
    
    # Create weather_db directory - ensure it's writable
    try:
        os.makedirs(weather_db_path, exist_ok=True)
        # Verify we can write to this directory with a test file
        test_file = os.path.join(weather_db_path, '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
    except (IOError, PermissionError) as e:
        # If we can't write to the specified path, fall back to /tmp in AWS Lambda
        if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
            fallback_path = '/tmp/weather_db'
            logger.warning(f"Cannot write to {weather_db_path}, falling back to {fallback_path}: {str(e)}")
            weather_db_path = fallback_path
            os.makedirs(weather_db_path, exist_ok=True)
        else:
            raise ValueError(f"Cannot write to directory {weather_db_path}: {str(e)}")
    
    logger.info(f"Using weather database path: {weather_db_path}")
    
    # Initialize or load last_update.json
    last_update_path = os.path.join(weather_db_path, "last_update.json")
    if os.path.exists(last_update_path):
        try:
            with open(last_update_path, 'r') as f:
                last_update = json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in {last_update_path}, recreating file")
            last_update = {}
    else:
        last_update = {}
    
    # Ensure date column is datetime
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    
    # Get date range from dataframe
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    # Check if we need historical data
    if min_date.date() < datetime.now().date():
        raise NotImplementedError("Historical weather data fetching not implemented yet")
    
    # Get unique locations
    locations = df['location'].unique()
    result_df = df.copy()
    
    # Process each location
    for location in locations:
        safe_location = location.lower().replace(', ', '_').replace(' ', '_')
        location_file = os.path.join(weather_db_path, f"{safe_location}.csv")
        needs_update = False
        
        # Check if we need to update the CSV
        if location in last_update:
            try:
                last_update_time = datetime.strptime(last_update[location], "%Y-%m-%d %H:%M:%S")
                # Update if older than 5 hours
                if (datetime.now() - last_update_time).total_seconds() > 18000:
                    needs_update = True
            except (ValueError, TypeError):
                needs_update = True
        else:
            needs_update = True
        
        # Check if CSV exists and contains required date range
        if os.path.exists(location_file):
            try:
                weather_df = pd.read_csv(location_file)
                if 'datetime' not in weather_df.columns:
                    needs_update = True
                else:
                    weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
                    if not (weather_df['datetime'].min() <= min_date and weather_df['datetime'].max() >= max_date):
                        needs_update = True
            except Exception as e:
                logger.warning(f"Error reading CSV file {location_file}: {str(e)}")
                needs_update = True
        else:
            needs_update = True
        
        # Update weather data if needed
        if needs_update:
            start = min_date.strftime("%Y-%m-%d")
            end = max_date.strftime("%Y-%m-%d")
            
            # Use more robust URL encoding that specifically handles commas and spaces
            # Replace spaces with + which works better for this API
            encoded_location = location.replace(' ', '+').replace(',', '%2C')
            
            # Use the full API URL with all necessary parameters
            url = (
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
                f"{encoded_location}/{start}/{end}?unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Ctemp%2Cfeelslike%2C"
                f"precip%2Csnow%2Cwindspeed%2Ccloudcover&include=days&key={api_key}&contentType=csv"
            )
            
            try:
                # Add a user agent to the request to avoid some HTTP errors
                headers = {'User-Agent': 'Mozilla/5.0'}
                req = urllib.request.Request(url, headers=headers)
                result_bytes = urllib.request.urlopen(req)
                csv_data = list(csv.reader(codecs.iterdecode(result_bytes, 'utf-8')))
                
                if not csv_data or len(csv_data) < 2:
                    logger.warning(f"No data received for {location}")
                    continue
                
                # Save new data
                new_data = pd.DataFrame(csv_data[1:], columns=csv_data[0])
                new_data.to_csv(location_file, index=False)
                
                # Update last_update.json
                last_update[location] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(last_update_path, 'w') as f:
                    json.dump(last_update, f, indent=4)
                    
            except Exception as e:
                logger.error(f"Error fetching weather data for {location}: {str(e)}")
                # Continue to the next location instead of raising an error
                continue
    
    # Merge weather data with input dataframe
    for location in locations:
        safe_location = location.lower().replace(', ', '_').replace(' ', '_')
        location_file = os.path.join(weather_db_path, f"{safe_location}.csv")
        
        if os.path.exists(location_file):
            try:
                weather_df = pd.read_csv(location_file)
                weather_df['datetime'] = pd.to_datetime(weather_df['datetime'])
                
                # Filter features if specified
                if features and all(f in weather_df.columns for f in features):
                    available_features = ['datetime'] + features
                    weather_df = weather_df[available_features]
                
                # Merge weather data for this location
                location_mask = result_df['location'] == location
                location_dates = result_df.loc[location_mask, 'date']
                
                for date in location_dates:
                    weather_row = weather_df[weather_df['datetime'].dt.date == date.date()]
                    if not weather_row.empty:
                        for col in weather_df.columns:
                            if col != 'datetime':
                                result_df.loc[(result_df['location'] == location) & 
                                            (result_df['date'] == date), f'weather_{col}'] = weather_row.iloc[0][col]
            except Exception as e:
                logger.error(f"Error processing weather data for {location}: {str(e)}")
                # Continue to the next location rather than failing
                continue
    
    return result_df
