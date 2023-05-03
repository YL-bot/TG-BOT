import requests
import aiohttp
import os
import asyncio

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


# функция для получения адреса по координатам
async def get_address_from_coords(coords):
    parametrs = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = await get_response("https://geocode-maps.yandex.ru/1.x/", parametrs)
        json_data = r
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        return "error in processing data - try again later"
