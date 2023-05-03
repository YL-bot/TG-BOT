import asyncio
import os

import aiohttp


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def random_event():
    req = await get_response('http://www.boredapi.com/api/activity/', {})
    data = req
    return data['activity']
    # img = data['data']['url']
    # return img


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# print(asyncio.run(random_event()))
