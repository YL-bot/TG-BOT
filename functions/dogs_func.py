import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def dogs():
    req = await get_response('https://dog.ceo/api/breeds/image/random', {})
    data = req
    img = data['message']
    return img


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
