# Использование API: http://numbersapi.com/<number>/<type>, где number — число, а type — тип факта
# (trivia — факт из жизни, math — математический факт, date и year — вопрос про дату (в формате MM/DD) и год).

import requests
import os
import asyncio
import aiohttp


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def get_date(data):
    try:
        month, day = data
        req = await get_response(f'http://numbersapi.com/{month}/{day}/date?json', {})
        text = req['text']
        return text

    except Exception:
        return 'Oooops, smth went wrong... :('


async def get_math(data):
    try:
        number = int(data[0])
        req = await get_response(f'http://numbersapi.com/{number}/math?json', {})
        text = req['text']
        return text

    except Exception:
        return 'Oooops, smth went wrong... :('


async def get_num(data):
    try:
        number = int(data[0])
        req = await get_response(f'http://numbersapi.com/{number}?json', {})
        text = req['text']
        return text

    except Exception:
        return 'Oooops, smth went wrong... :('

# print(asyncio.run(get_date(('erer', 'erer'))))
# print(asyncio.run(get_math('erer')))
# print(asyncio.run(get_num('fsdfds')))
