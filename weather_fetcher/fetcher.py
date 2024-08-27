import os
from dotenv import load_dotenv
from httpx import AsyncClient

import crud
from db import models


load_dotenv(".env")

API_GEO_URL = os.getenv("API_GEO_URL")
API_WEATHER_URL = os.getenv("API_WEATHER_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_cities(db):
    return crud.get_all_cities(db)


def save_temperature(db, city_id, temperature):
    db_temp = models.DBTemperature(city_id=city_id, temperature=temperature)
    db.add(db_temp)
    db.commit()


async def get_location(city: str, client: AsyncClient):
    parameters = {"q": city, "appid": WEATHER_API_KEY, "units": "metric", "lang": "ua"}
    response = await client.get(f"{API_GEO_URL}/direct", params=parameters)
    if response.status_code == 200:
        lat = response.json()[0]["lat"]
        lon = response.json()[0]["lon"]
        return await get_weather(lat, lon, client)
    else:
        return False


async def get_weather(lat, lon, client: AsyncClient):
    parameters = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ua",
    }

    response = await client.get(f"{API_WEATHER_URL}/weather", params=parameters)

    if response.status_code == 200:
        return response.json()["main"]["temp"]
    else:
        return False


async def main(db):
    async with AsyncClient() as client:
        temp = {
            city.id: await get_location(city.name, client) for city in get_cities(db)
        }

        for temperature in temp.items():
            save_temperature(db, city_id=temperature[0], temperature=temperature[1])
