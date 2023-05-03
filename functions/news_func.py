import requests
import os
import asyncio
import aiohttp

key = 'ee08b2ab12084bfa9bba25faacd4e831'

categories_list = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
country_list = ['ch', 'ru', 'fr', 'de', 'us', 'en']


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def get_news(category, country):
    global key, categories_list, country_list

    req = await get_response('https://newsapi.org/v2/top-headlines?',
                             params={'country': country, 'category': category, 'pageSize': 21, 'apiKey': key})
    data = req
    # print(data)
    text = 'Here u r: \n\n'

    try:
        for i in range(0, 5):
            title = data['articles'][i]['title']
            desc = data['articles'][i]['description']
            s_url = data['articles'][i]['url']

            if desc is not None:
                text += f'----\n\nTitle: {title}\n\nDescription: {desc}\n\nUrl: {s_url} \n\n'

            else:
                text += f'----\n\nTitle: {title}\n\nUrl: {s_url} \n\n'

        return text

    except Exception as e:
        if text == 'Here u r: \n\n':
            return 'Oops, smth went wrong... :('
        return text


async def get_spec_news(about):
    global key

    try:
        text = 'Here u r: \n\n'

        req = await get_response('https://newsapi.org/v2/top-headlines?', params={'q': about, 'apiKey': key})
        data = req

        if not data:
            raise Exception

        for i in range(0, 5):
            title = data['articles'][i]['title']
            desc = data['articles'][i]['description']
            s_url = data['articles'][i]['url']

            if desc is not None:
                text += f'----\n\nTitle: {title}\n\nDescription: {desc}\n\nUrl: {s_url} \n\n'

            else:
                text += f'----\n\nTitle: {title}\n\nUrl: {s_url} \n\n'

        return text

    except Exception:
        if text == 'Here u r: \n\n':
            return 'Oops, smth went wrong... :('

        return text
