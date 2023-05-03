import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def kitties():
    req = await get_response('https://api.thecatapi.com/v1/images/search', {})
    data = req
    img = data[0]['url']
    return img


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
