# Exercise

## *Weather monitoring app*

Choose a free open weather forecast API of your preference and get a weather forecast for the next few days(config to
the application). If the temperature lies outside the minimum and maximum temperature limits then we need to capture
that and visually present that to the user on a map with some dots and hovering would give the deviations.

REST API to get the information should be available.

Requirements:

1. REST API for the back end to add, remove, set, and query various data points towards the back end.
2. The app configuration is a JSON that can be used for customizations. Ex: Default number of days to forecast
3. The application will have persistence with the use of a NoSQL database.
4. Proper logging mechanism.
5. Minimal test case to validate the functionality
6. Documentation for the finished application.

Minimum Inputs:

1. Name of the Location
2. Longitude
3. Latitude
4. Min temperature
5. Max temperature

---

# Solution Design

## High level diagram

![Image Alt Text](HLD.jpeg)

## Components:

### 1.Forcast-API:

- This external service provides weather forecasts based on user queries.
- The app communicates with the Forecast-API to retrieve weather data.
- Here I chose the [Open-Meteo](https://open-meteo.com/)
- RESTful endpoints are available for querying weather information.
    - Location Search
    - Weather data of specific location before and after N days. `(0 < N <= 7)`

### 2. Backend - FastAPI:

- The central component of the app.
- Responsible for handling user requests, data processing, and interaction with other components.
- Provides REST APIs for querying DB, Forcast API calls, and for processing.
- Utilizes FastAPI for better Documentation, Playground experience and asynchronous communication.
- Also enabled the unittests for the process functions on this project.

  #### Endpoints:

- **`GET /default_map`**:<br>
    - If DB is connected, then this endpoint returns all the coordinates in DB on the current date.
    - If there is no DB, then this will return the temperature of the default location mentioned in the conf.


- **`GET /location_search`**:<br>
    - The location_search endpoint will search the location with the name sting.
    - It is internally calling the Open-Meteo API.
    - It gives the list of suggested locations with coordinates based on the search keyword.


- **`POST /forcast_temperature`**:<br>
    - The input for the _forcast_temperature_ endpoint is partially from the chosen location of */location_search*
      endpoint.
    - The rest input fields like start_date, end_date, max_temperature_limit and min_temperature_limit is from the user.
    - Based on the input, it will fetch the forcast data from the Open-Meteo API.
    - Then finally process on results for the deviation status and return it.

  <br>Detailed documentation and Playground for all API Endpoints will get in the following links:
  - Documentation: http://localhost:8000/documentation
  - Playground: http://localhost:8000/playground


### 3. UI-Angular:

- The front-end framework for building the user interface.
- Displays weather forecasts and temperature deviations of the given coordinates.
- Allows users to input location and choose the right one from the given suggestions.
- Interacts with the Backend-FastAPI via RESTful endpoints.
  #### Pages:
- **`HomePage`**:<br>
    - Shows the default map of current-date without any deviation data.
    - The default Map consist of many coordinates as highlighted locations.
    - Also it includes the user input section of _location_,_latitude_, _longitude_, _start_date_, _end_date_,
      _max_temp_limit_ and _min_temp_limit_.
- **`UpadtedMapPage`**:<br>
    - It will be the same homepage structure.
    - The map data will update based on the forecasted data of the specific location.
    - While hovering on the location dot, there will be a popup for showing the deviation status for the resultant
      dates.

### 4. NoSql-MongoDB:

- A NoSQL database used for data persistence.
- Stores historical weather data results that fetches from the open API.
- Ensures data availability and reliability.<br>
<br>
  **`Note`**: I handled this application to run without MongoDB instance.<br>
  If the DB is not found, then the data calls will always depend on the Open Meteo API.

### 5. Logging :- FileHandler & StreamHandlers:

- For logging, I implemented file handler logging mechanism to save the logs to the given file.
- All the logs from the app will write to the `fast_api.log` file.
- Also implemented a streamHandler to log the data on the running stream itself.