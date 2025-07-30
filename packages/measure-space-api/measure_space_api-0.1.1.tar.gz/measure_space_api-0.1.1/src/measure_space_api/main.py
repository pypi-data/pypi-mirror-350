import os
import requests
import pandas as pd
from typing import Dict, Any, Union, Tuple
from .constants import URL_MAPPING

def call_api(
    api_key: str,
    api_url: str,
    params: Dict[str, Any],
    return_json: bool=True,
) -> Union[Dict[str, Any], pd.DataFrame]:
    """Base API call function.

    Parameters
    ----------
    api_key : str
        API key.
    api_url : str
        URL of the API or API endpoint.
    params : Dict[str, Any]
        A dictionary of API parameters. 
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.

    Raises
    ------
    RuntimeError
        API error information witch response text and status code.
    """
    base_url = api_url
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if return_json:
            return data
        else:
            return pd.DataFrame(data)
    else:
        raise RuntimeError(f"API Error: {response.status_code} - {response.text}")

def call_api_with_location(
        api_name: str,
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]=None,
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get hourly weather forecast for given latitude and longitude or location name.

    Parameters
    ----------
    api_name : str
        API or API endpoint name from URL_MAPPING variable in constants.py.
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default None. For example, it can be the following for 
        the hourly weather API: params = {'variables': 'tp, t2m', 'unit': 'metric', 'local_flag': True}
        Each API or API endpoint has different format. Details can be found at https://measurespace.io/api-explorer. 
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    if location_name:
        # call geocoding API to get lat and lon info
        lat, lon = get_lat_lon_from_city(geocoding_api_key, location_name)
    else:
        lat, lon = latitude, longitude
    
    params["latitude"] = lat
    params["longitude"] = lon

    return call_api(
        api_key,
        URL_MAPPING[api_name],
        params=params,
        return_json=return_json,
    )

def get_lat_lon_from_city(api_key: str, location_name: str) -> Tuple[float, float]:
    """Get latitude and longitude info for a given city.

    Parameters
    ----------
    api_key : str
        API key.
    location_name : str
        Name of the location, by default None. For example, "New York" or "Beijing, China"

    Returns
    -------
    Tuple[float, float]
        Latitude and longitude.
    """

    params = {
        'query': location_name,
        'limit': 1,
        }
    
    res = call_api(api_key, URL_MAPPING['geocoding_autocomplete'], params)

    if "results" in res and res['results'][0]:
        lat, lon = res['results'][0]['lat'], res['results'][0]['lon']
    else:
        lat, lon = None, None

    return lat, lon

def get_city_from_lat_lon(api_key: str, latitude: float, longitude: float) -> str:
    """Get latitude and longitude info for a given city.

    Parameters
    ----------
    api_key : str
        API key.
    latitude : float
        Latitude.
    longitude : float
        Longitude.

    Returns
    -------
    str
        Name of the nearest city regarding given latitude and longitude.
    """

    params = {
        'lat': latitude,
        'lon': longitude,
        'limit': 1,
        }
    
    res = call_api(api_key, URL_MAPPING['geocoding_nearest_city'], params)

    if "results" in res and res['results'][0]:
        return res['results'][0]
    else:
        return "Not Found"

def get_hourly_weather(
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]={'variables': 'tp, t2m', 'unit': 'metric'},
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get hourly weather forecast for given latitude and longitude or location name.

    Parameters
    ----------
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default {'variables': 'tp, t2m', 'unit': 'metric'}.
        Details can be found at https://measurespace.io/api-explorer. 
        Variable names and meaning can be found at https://measurespace.io/documentation#global-hourly-weather-forecast-variables.
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    
    return call_api_with_location(
        'hourly_weather',
        api_key,
        geocoding_api_key,
        location_name,
        latitude,
        longitude,
        params,
        return_json,
    )

def get_daily_weather(
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]={'variables': 'tp, minT, maxT', 'unit': 'metric'},
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get daily weather forecast for given latitude and longitude info or location name.
    
    Parameters
    ----------
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default {'variables': 'tp, minT, maxT', 'unit': 'metric'}.
        Details can be found at https://measurespace.io/api-explorer. 
        Variable names and meaning can be found at https://measurespace.io/documentation#global-daily-weather-forecast-variables.
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    
    return call_api_with_location(
        'daily_weather',
        api_key,
        geocoding_api_key,
        location_name,
        latitude,
        longitude,
        params,
        return_json,
    )

def get_daily_climate(
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]={'variables': 'tp, tmin, tmax', 'unit': 'metric'},
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get daily climate forecast for given latitude and longitude info or location name.
    
    Parameters
    ----------
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default {'variables': 'tp, t2m', 'unit': 'metric'}.
        Details can be found at https://measurespace.io/api-explorer. 
        Variable names and meaning can be found at https://measurespace.io/documentation#global-climate-forecast-variables.
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    
    return call_api_with_location(
        'daily_climate',
        api_key,
        geocoding_api_key,
        location_name,
        latitude,
        longitude,
        params,
        return_json,
    )

def get_hourly_air_quality(
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]={'variables': 'AQI, DP'},
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get hourly air quality forecast for given latitude and longitude info or location name.
    
    
    Parameters
    ----------
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default {'variables': 'AQI, DP'}.
        Details can be found at https://measurespace.io/api-explorer. 
        Variable names and meaning can be found at https://measurespace.io/documentation#https://measurespace.io/documentation#global-hourly-air-quality-forecast-variables.
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    
    return call_api_with_location(
        'hourly_air_quality',
        api_key,
        geocoding_api_key,
        location_name,
        latitude,
        longitude,
        params,
        return_json,
    )

def get_daily_air_quality(
        api_key: str, 
        geocoding_api_key: str=None, 
        location_name: str=None, 
        latitude: float=None, 
        longitude: float=None, 
        params: Dict[str, Any]={'variables': 'AQI'},
        return_json: bool=True,
        ) -> Union[Dict[str, Any], pd.DataFrame]:
    """Get daily air quality forecast for given latitude and longitude info or location name.
    
    
    Parameters
    ----------
    api_key : str
        API key.
    geocoding_api_key : str, optional
        API key for geocoding API, by default None. This is required if calling other APIs using location names.
    location_name : str, optional
        Name of the location, by default None. For example, "New York" or "Beijing, China"
    latitude : float, optional
        Latitude, by default None
    longitude : float, optional
        Longitude, by default None
    params : Dict[str, Any], optional
        A dictionary of API parameters, by default {'variables': 'AQI, maxPM25'}.
        Details can be found at https://measurespace.io/api-explorer. 
        Variable names and meaning can be found at https://measurespace.io/documentation#https://measurespace.io/documentation#global-hourly-air-quality-forecast-variables.
    return_json : bool, optional
        return data in json format or pandas dataframe format, by default True which returns json format.

    Returns
    -------
    Union[Dict[str, Any], pd.DataFrame]
        API response in json or pandas dataframe format.
    """
    
    return call_api_with_location(
        'daily_air_quality',
        api_key,
        geocoding_api_key,
        location_name,
        latitude,
        longitude,
        params,
        return_json,
    )

    
