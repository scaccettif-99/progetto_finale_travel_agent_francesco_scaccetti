# weather_finder.py
import requests
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Optional


class WeatherInput(BaseModel):
    city: str = Field(description="The city to get the weather for.")
    start_date: str = Field(description="The start date of the trip (YYYY-MM-DD) e.g. 2024-12-13.")
    end_date: str = Field(description="The end date of the trip (YYYY-MM-DD) e.g. 2024-12-19.")


class WeatherInputSchema(BaseModel):
    params: WeatherInput


@tool(args_schema=WeatherInputSchema)
def weather_finder(params: WeatherInput) -> str:
    """
    This tool retrieves the weather forecast for a city and a date range.
    Use it when the user asks about the weather at their destination.
    """
    try:
        # coordinate citta'
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": params.city, "count": 1, "language": "it"},
        )
        location = geo_response.json()["results"][0]
        city_name = location["name"]
        lat = location["latitude"]
        lon = location["longitude"]

        # api meteo 
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "start_date": params.start_date,
                "end_date": params.end_date,
                "timezone": "auto",
            },
        )
        data = weather_response.json()["daily"]

        giorni = []
        for i in range(len(data["time"])):
            giorni.append(
                f"📅 {data['time'][i]}: "
                f"🌡️ {data['temperature_2m_min'][i]}°C – {data['temperature_2m_max'][i]}°C, "
                f"🌧️ Pioggia: {data['precipitation_sum'][i]}mm"
            )

        result = f"Previsioni meteo per {city_name}:\n"+ "\n".join(giorni)

    except Exception as e:
        result = str(e)

    print("*" * 80)
    print("weather_finder")
    print(f"  City: {params.city} | From {params.start_date} to {params.end_date}")
    print("*" * 80)

    return result
