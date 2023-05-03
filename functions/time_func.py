# возвращает самые популярные города со временем
# также возвращает местное время

import os
import asyncio
import requests
import aiohttp


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def time():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    list_zones = ['Europe/London', 'Europe/Moscow', 'Europe/Berlin',
                  'America/Los_Angeles', 'America/Toronto',
                  'Asia/Dubai', 'Asia/Hong_Kong', 'Asia/Tokyo',
                  'Africa/Lagos'
                  ]

    txt = 'The time of our vast planet:\n\n'

    for i in list_zones:
        req = await get_response("https://timeapi.io/api/Time/current/zone?", params={'timeZone': i})

        data = req

        txt += f"{i.split('/')[1]} : {data['time']} \n"

    txt += "\nHaven't found the right time? Follow the link bellow!\n\nhttps://www.timeanddate.com/worldclock/?low=c"

    return txt


def main():
    return asyncio.run(time())
