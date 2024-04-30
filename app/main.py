import json
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient

from .models import ForcastTemperature, LocationListResponse, LocationSearchResponse, LocationSearchResult, \
    ForcastTemperatureResponse
from .utils import get_weather_data, get_location_data, get_deviation_status

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
    with open("/code/app/DEFAULT_LOCATION.json", 'r') as file:  # Default conf location
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
         name="Default Map Data",
         description="Returns a Map data for the locations in DB. If DB is not accessible it will show the default location",
         response_model=LocationListResponse,
         responses={
             200: {"description": "Valid response as a JSON format."},
             429: {"description": "Too many requests"},
             404: {"description": "Not found error!"}
         })
async def get_default_map(date=None):
    # todo: Handle TimeZones
    date = datetime.now().strftime("%Y-%m-%d") if not date else date
    # Approach1: Fetch from DB for the current date
    if hasMongoObj:
        result_obj = temp_collection.find({"date": date})
        weather_dataset = []
        for weather_data in result_obj:
            doc_ = ForcastTemperatureResponse(**weather_data)
            weather_dataset.append(doc_.dict())

        if weather_dataset:
            logger.info(f"Results fetched from MongoDB for the date {date}")
            return JSONResponse(content=weather_dataset)
        logger.warning(f"No results found from MongoDB for date {date}")

    # Approach 2: Fetch temperature of Default location for the current date via API.
    weather_dataset = get_weather_data(lat=default_location['latitude'],
                                       long=default_location['latitude'],
                                       location=default_location['location'],
                                       start_date=date, end_date=date)
    if not weather_dataset:
        logger.warning(f"No weather data found for Default location: {default_location}")
        raise HTTPException(status_code=404, detail="Data Not Found!")
    logger.info(f"Results fetched from API for the location {default_location['location']}")
    return JSONResponse(content=weather_dataset)


@app.get("/location_search",
         name="Location name search.",
         description="Location search API. It is Internally calling the open-meteo location search API",
         response_model=LocationSearchResponse,
         responses={
             200: {"description": "Valid response as a JSON format."},
             429: {"description": "Too many requests"},
             404: {"description": "Server error!"},
             204: {"description": "Data not found for the location!"}
         })
async def location_search_by_name(name):
    locations = get_location_data(name=name)
    # checking the response types
    if isinstance(locations, int):
        raise HTTPException(status_code=locations)
    elif isinstance(locations, list):
        results = []
        for doc in locations:
            doc['location'] = doc.pop('name')
            doc_ = LocationSearchResult(**doc)
            results.append(doc_.dict())
        return JSONResponse(content=results)
    else:
        raise HTTPException(status_code=404, detail="Server Error")


@app.post(
    "/forcast_temperature",
    name="Temperature deviation check",
    description="Temerature forcast for the given days. It will take a minimum threshold temperature and maximum threshold temperature. Then returns the deviation status of of actual temperature.",
    response_model=LocationListResponse,
    responses={
        200: {"description": "Valid response as a JSON format."},
        429: {"description": "Too many requests"},
        404: {"description": "Not found error!"},
        204: {"description": "Data not found for the location!"}
    }
)
async def forcast_temperature_data(payload: ForcastTemperature):
    weather_dataset = get_weather_data(lat=payload.latitude,
                                       long=payload.longitude,
                                       location=payload.location,
                                       start_date=payload.start_date, end_date=payload.end_date)

    if not weather_dataset:
        logger.warning(f"No weather data found for given payload: {payload}")
        raise HTTPException(status_code=404, detail="Data Not Found!")

    # Write responses to MongoDB
    for weather_data in weather_dataset:
        if hasMongoObj:
            upsert_temperature(weather_data)
        # check for deviation:
        weather_data['deviation_status'] = get_deviation_status(
            max_temp=weather_data['max_temperature'],
            min_temp=weather_data['min_temperature'],
            max_limit=payload.max_temperature,
            min_limit=payload.min_temperature
        )

    return JSONResponse(content=weather_dataset)
