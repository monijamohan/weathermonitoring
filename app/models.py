from pydantic import BaseModel, Field


class DailyTemperature(BaseModel):
    location: str = Field(
        title="Location from the given sample",
        examples=["DWD Germany", "NOAA US"],
        default="forcast")
    latitude: float = Field(
        title="Latitude of the coordinate",
        examples=[52.52, 56.34]
    )
    longitude: float = Field(
        title="Longitude of the coordinate",
        examples=[13.41, 14.65]
    )
