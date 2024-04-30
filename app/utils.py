import hashlib
import logging as logger
import traceback

import requests


def _generate_unique_id(date, latitude, longitude):
    combined_str = f"{date}_{latitude}_{longitude}"
    hash_obj = hashlib.sha256(combined_str.encode())
    unique_id = hash_obj.hexdigest()
    return unique_id


def get_weather_data(lat, long, location=None, start_date=None, end_date=None):
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
            day_data['doc_id'] = _generate_unique_id(day_data['date'], str(day_data['latitude']),
                                                     str(day_data['longitude']))
            weather_data_set.append(day_data)
    except Exception as ex:
        logger.error(traceback.format_exc())
        raise ex
    return weather_data_set
