import aiohttp
import asyncio
import os


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def jokes_chak():
    req = await get_response('https://geek-jokes.sameerkumar.website/api?', {'format': 'json'})
    data = req
    answer = data['joke']
    return answer


async def jokes_panch():
    req = await get_response('https://official-joke-api.appspot.com/random_joke', {})
    data = req
    setup = data['setup']
    punchline = data['punchline']

    return f'Setup:\n{setup}\n\nPunchline:\n{punchline}'


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
