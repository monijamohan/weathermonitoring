from pydantic import BaseModel, Field


class ForcastTemperature(BaseModel):
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
    start_date: str = Field(
        title="Date in string format.",
        examples=["2024-04-30", "2024-05-01"]
    )
    end_date: str = Field(
        title="Date in string format.",
        examples=["2024-05-03", "2024-05-06"]
    )

    min_temperature: float = Field(
        title="Minimum threshold temperature",
        examples=[7.95093, 4.65]
    )

    max_temperature: float = Field(
        title="Maximum threshold temperature",
        examples=[25.95093, 28.65]
    )

