from typing import List

from pydantic import BaseModel, Field


class LocationMeta(BaseModel):
    location: str = Field(
        title="Location from the given sample",
        examples=["Sollentuna", "Delhi"]
    )
    latitude: float = Field(
        title="Latitude of the coordinate",
        examples=[59.42804, 56.34]
    )
    longitude: float = Field(
        title="Longitude of the coordinate",
        examples=[17.95093, 14.65]
    )


class LocationSearchResult(LocationMeta):
    country: str = Field(
        title="Country name", \
        examples=["Sweden", "United States"]
    )


class LocationAPI(LocationMeta):
    min_temperature: float = Field(
        title="Minimum threshold temperature",
        examples=[7.95093, 4.65]
    )

    max_temperature: float = Field(
        title="Maximum threshold temperature",
        examples=[25.95093, 28.65]
    )


class ForcastTemperature(LocationAPI):
    start_date: str = Field(
        title="Date in string format.",
        examples=["2024-04-30", "2024-05-01"]
    )
    end_date: str = Field(
        title="Date in string format.",
        examples=["2024-05-03", "2024-05-06"]
    )


class ForcastTemperatureResponse(LocationAPI):
    date: str = Field(
        title="Date in string format.",
        examples=["2024-05-03", "2024-05-06"]
    )
    doc_id: str = Field(
        title="Doc-Id created by combination of 'DATE_LATITUDE_LONGITUDE' ",
        examples=["2e0e3929260060dc2b04062f5b7229ad5d9606d323b545273139dfce0c1b6f0e",
                  "29ad5d9606d323b545273139dfce0c1b6f0e"]
    )


LocationListResponse = List[ForcastTemperatureResponse]
LocationSearchResponse = List[LocationSearchResult]
