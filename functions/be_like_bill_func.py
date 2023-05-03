import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


# bill and text
async def bill_text(txt):
    req = await get_response('https://belikebill.ga/billgen-API.php?', {'text': txt})
    data = req
    print(data)
    return ""


# bill and name
async def bill_name(text):
    req = await get_response('https://belikebill.ga/billgen-API.php?', {'default': 1, 'name': text})
    data = req
    print(data)
    return ""


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# asyncio.run(bill_text('Капибара ао'))
