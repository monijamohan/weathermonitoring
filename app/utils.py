from pymongo import MongoClient

# Todo: Enable Retry Connection Pool
mongo_client = MongoClient('mongodb://host.docker.internal:27017/') # On local docker instance if the DB is in same server
temp_collection = mongo_client.weatherdata.temperature
