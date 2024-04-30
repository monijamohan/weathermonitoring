import json
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from .utils import get_weather_data

logger = logging.getLogger()

# MongoDB Connection Initialize
# # Todo: Enable Retry Connection Pool
logger.info("MongoConnection initiated...")
try:
    # Assuming a MongoDB is up in the localhost. Also expecting a 'weatherdata' DB and 'temperature' Collection in it.
    mongo_client = MongoClient(
        'mongodb://host.docker.internal:27017/')  # On local docker instance if the DB is in same server

    if not 'weatherdata' in mongo_client.list_database_names():
        temp_collection = None
    db = mongo_client['weatherdata']
    logger.info(f"CollectionNames: {db.list_collection_names()}")
    if 'temperature' in db.list_collection_names():
        logger.info(f"CollectionNames: {db.list_collection_names()}")
    temp_collection = db.temperature
    hasMongoObj = True
except Exception:
    # logger.warning(traceback.format_exc())
    logger.warning("Mongo Connection Failed! Skipping MongoDB related operations!")
    hasMongoObj = False
# todo : defaultlocation to exception
with open("/code/app/DEFAULT_LOCATION.json", 'r') as file:  # Default location conf
    logger.info("Reading DEFAULT_LOCATION.json ...")
    default_location = json.load(file)

def upsert_temperature(temperature_data):
    result = temp_collection.update_one({'uniqueId': temperature_data['doc_id']}, {'$set': temperature_data},
                                        upsert=True)
    if result.upserted_id is not None:
        logger.info(f"New document inserted with unique ID: {temperature_data['doc_id']}")
    else:
        logger.info(f"Existing document updated with unique ID: {temperature_data['doc_id']}")


# FastAPI Connection Initialize
app = FastAPI(
    title="Weather Forcast APIs",
    redoc_url="/documentation",
    docs_url="/playground",
    version=open("VERSION.txt").read().strip()
)

@app.get("/default_map",
         name="Default Map for the home page",
         description="Returns a Map data for the locations in DB. If DB is not accessible it will show the default location",
         # response_model=ResponseHomeMap,
         responses={
             200: {"description": "Valid response as a JSON format."},
             429: {"description": "Too many requests"},
             404: {"description": "No data found from API!"}
         })
async def get_default_map(date=None):
    # todo: Handle TimeZones
    date = datetime.now().strftime("%Y-%m-%d") if not date else date
    # Approach1: Fetch from DB for the current date
    if hasMongoObj:
        #todo:
        result_obj = temp_collection.find({"date": date})
        weather_dataset = []
        for weather_data in result_obj:
            weather_data['uniqueId'] = str(weather_data.pop('_id'))
            weather_dataset.append(weather_data)
        if weather_dataset:
            logger.info(f"Results fetched from MongoDB for the date {date}")
            return JSONResponse(content=weather_dataset)
        logger.warning(f"No results found from MongoDB for date {date}")

    # Approach 2: Fetch temperature of Default location for the current date via API.
    weather_dataset = get_weather_data(lat=default_location['latitude'],
                                       long=default_location['latitude'],
                                       location=default_location['name'],
                                       start_date=date, end_date=date)
    if not weather_dataset:
        logger.warning(f"No weather data found for Default location: {default_location}")
        raise HTTPException(status_code=404, detail="Data Not Found!")
    logger.info(f"Results fetched from API for the location {default_location['name']}")
    # for weather_data in weather_dataset:
    #     upsert_temperature(weather_data)
    return JSONResponse(content=weather_dataset)