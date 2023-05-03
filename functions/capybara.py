import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


# рандомная картинка капибары
async def capybara_img():
    req = await get_response('https://api.capy.lol/v1/capybara?json=true', {})
    data = req
    img = data['data']['url']
    return img


async def capybara_fact():
    req = await get_response('https://api.capy.lol/v1/fact', {})
    data = req
    img = data['data']['fact']
    return img


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
