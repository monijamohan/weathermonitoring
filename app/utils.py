import hashlib
import traceback
import requests
from app import logger

def generate_unique_id(date, latitude, longitude):
    """
    Creating uniqueId to handle the duplicated entries in MongoDB document collection.

    """
    combined_str = f"{date}_{latitude}_{longitude}"
    hash_obj = hashlib.sha256(combined_str.encode())
    unique_id = hash_obj.hexdigest()
    return unique_id


def get_location_data(name):
    """
    Location Search on open-meteo API
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count=5&language=en&format=json"
    resp = requests.get(url)
    if resp.status_code != 200:
        logger.error(f"Request failed for the Location API {url}")
        return resp.status_code
    logger.info(f"Got 200 response for Location API {url}")

    resp_data = resp.json()
    if not resp_data.get('results'):
        logger.warning(f"No data found for Location API {url}")
        return 204  # No data found status
    else:
        return resp_data['results']


def get_weather_data(lat, long, location=None, start_date=None, end_date=None):
    """
    WeatherData fetch on Open-Meteo API
    """
    url = "https://api.open-meteo.com/v1/forecast?" \
          f"latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min"
    if start_date and end_date:
        url += f"&start_date={start_date}&end_date={end_date}"
    logger.info(f"Request initiated to the Forcast API {url}")
    resp = requests.get(url=url)
    if resp.status_code != 200:
        logger.error(f"Request failed for the Forcast API {url}")
        return
    logger.info(f"Got 200 response for Forcast API {url}")
    try:
        resp_data = resp.json()
        weather_data_set = []
        for idx, date in enumerate(resp_data['daily']['time']):
            day_data = {"date": date,
                        "latitude": resp_data['latitude'],
                        'longitude': resp_data['longitude'],
                        "min_temperature": resp_data['daily']["temperature_2m_min"][idx],
                        "max_temperature": resp_data['daily']["temperature_2m_max"][idx],
                        "location": location
                        }
            day_data['doc_id'] = generate_unique_id(day_data['date'], str(day_data['latitude']),
                                                     str(day_data['longitude']))
            weather_data_set.append(day_data)
    except Exception as ex:
        logger.error(traceback.format_exc())
        raise ex
    return weather_data_set


def get_deviation_status(max_temp, min_temp, max_limit, min_limit):
    if (max_temp > max_limit) and (min_temp < min_limit):
        return "increased&decreased"
    elif max_temp > max_limit:
        return "increased"
    elif min_temp < min_limit:
        return "decreased"
    else:
        return "normal"
