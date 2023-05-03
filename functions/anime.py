import asyncio
import os

import aiohttp

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
          'декабря']


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def find_anime(key_word):
    req = await get_response(f'https://kitsu.io/api/edge/anime?filter[text]={key_word}', {})
    data = req
    results = 10 if len(data['data']) >= 10 else len(data['data'])
    if results > 0:
        text = f'Вот {results} результатов по запросу {key_word}:\n'
        count = 0
        for i in data['data']:
            count += 1
            text += f'{count}){i["attributes"]["canonicalTitle"]}, id - {i["id"]}\n'
    else:
        return f'Не найдено тайтлов по поиску "{key_word}", введите заново', 0
    return text, 1


async def find_anime_id(anime_id):
    req = await get_response(f'https://kitsu.io/api/edge/anime?filter[id]={anime_id}', {})
    data = req
    text = ''
    if len(data['data']) > 0:
        find = data['data'][0]
        title = find["attributes"]["canonicalTitle"]
        idd = find["id"]
        img = find["attributes"]["posterImage"]["original"]
        start_date = find["attributes"]["startDate"].split('-')
        end_date = find["attributes"]["endDate"].split('-')
        age_rating = find["attributes"]["ageRating"]
        episode_count = find["attributes"]["episodeCount"]
        episode_length = find["attributes"]["episodeLength"]
        text += f'{title}\n\n' \
                f'id: {idd}\n' \
                f'Дата выхода: {start_date[2]} {months[int(start_date[1]) - 1]} {start_date[0]}\n' \
                f'Дата окончания: {end_date[2]} {months[int(end_date[1]) - 1]} {end_date[0]}\n' \
                f'Возрастной рейтинг: {age_rating}\n' \
                f'Количество эпизодов: {episode_count}\n' \
                f'Длина эпизода: {episode_length} мин\n\n' \
                f'{img}'
    else:
        return 'Неправильно введён id, пожалуйста повторите', 0
    return text, 1


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# print(asyncio.run(find_anime('jujutsu'))[0])
# print(asyncio.run(find_anime_id('dsfsdfsd'))[0])
