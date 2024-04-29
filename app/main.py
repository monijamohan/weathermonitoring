import hashlib
import logging
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .models import DailyTemperature
from .utils import temp_collection


# # Config Default # To log in the Running container
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()],
)

# # Configure the logger | File Handler
file_handler = logging.FileHandler('fast_api.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
logging.getLogger().addHandler(file_handler)

app = FastAPI(
    title="Weather Forcast APIs",
    redoc_url="/documentation",
    docs_url="/playground",
    version=open("VERSION.txt").read().strip()
)

_location_map = {
    "DWD Germany": "dwd-icon",
    "NOAA US": "gfs"
    # todo: add rest locations
}


def generate_unique_id(date, latitude, longitude):
    combined_str = f"{date}_{latitude}_{longitude}"
    hash_obj = hashlib.sha256(combined_str.encode())
    unique_id = hash_obj.hexdigest()
    return unique_id


def get_weather_data(location, lat, long, start_date=None, end_date=None):
    url = "https://api.open-meteo.com/v1/" + \
          f"{_location_map.get(location, 'forcast')}?" \
          f"latitude={lat}&longitude={long}&daily=temperature_2m_max,temperature_2m_min"
    if start_date and end_date:
        url += f"start_date={start_date}&end_date={end_date}"
    # print(url)
    resp = requests.get(url=url)
    # todo validate response
    resp_data = resp.json()
    # print(f"""----\n\n-----{resp_data}""")
    weather_data = []
    for idx, date in enumerate(resp_data['daily']['time']):
        day_data = {"date": date,
                    "latitude": resp_data['latitude'],
                    'longitude': resp_data['longitude'],
                    "min_temperature": resp_data['daily']["temperature_2m_min"][idx],
                    "max_temperature": resp_data['daily']["temperature_2m_max"][idx]}
        day_data['doc_id'] = generate_unique_id(day_data['date'], str(day_data['latitude']), str(day_data['longitude']))
        weather_data.append(day_data)
    return weather_data


@app.post("/daily_temperature/")
async def write_daily_temperature(inputs: DailyTemperature):
    logging.info(f"daily_temperature input params are : {str(inputs)}")
    weather_dataset = get_weather_data(location=inputs.location, lat=inputs.latitude, long=inputs.longitude) # todo: add start_Date and end_Date
    for w_data in weather_dataset:
        result = temp_collection.update_one({'uniqueId': w_data['doc_id']}, {'$set': w_data}, upsert=True)
        if result.upserted_id is not None:
            logging.info(f"New document inserted with unique ID: {w_data['doc_id']}")
        else:
            logging.info(f"Existing document updated with unique ID: {w_data['doc_id']}")

    # Todo: update response type

    weather_dataset = temp_collection.find_one()
    weather_dataset['_id'] = str(weather_dataset.pop('_id'))
    return JSONResponse(content=weather_dataset)
