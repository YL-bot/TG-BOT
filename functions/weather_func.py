# ищет погоду в месте запроса
import requests
import asyncio
import aiohttp

app_id = '9679c05520936f7d691139a917576317'


async def get_response(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def moji(txt):
    dict_m = {
        'Thunderstorm': '🌩',
        'Drizzle': '🌦',
        'Rain': '🌧',
        'Snow': '🌨',
        'snow': '🌨',
        'Clear': '☀️',
        'Clouds': '🌥'
    }

    try:
        return dict_m[txt]

    except Exception:
        return '🌫'


async def weather(coords):
    req = await get_response("https://api.openweathermap.org/data/2.5/weather?",
                             params={'lat': coords[1], 'lon': coords[0], 'units': 'metric', 'lang': 'en',
                                     'APPID': app_id})

    # 'lang': 'ru' для ru версии

    data = req

    dictt = {}

    dictt['weather'] = data['weather'][0]['description']
    dictt['temperature'] = data['main']['feels_like']

    sp = data['wind']['speed']
    d = data['wind']['deg']

    dictt['wind'] = f"{sp} m/sec ; {d} deg"
    dictt['visibility'] = str(int(data['visibility']) / 1000)
    dictt['humidity'] = data['main']['humidity']

    dictt['png'] = await moji(data['weather'][0]['main'])

    txt = f"Oh, here u r:\n\n {dictt['png']}\n\n {dictt['weather'].capitalize()} \n\n Feels like: {dictt['temperature']} C \n Wind: {dictt['wind']} \n Visibility: {dictt['visibility']} km \n Humidity: {dictt['humidity']} %\n"

    return txt

# https://yandex.ru/dev/weather/doc/dg/concepts/about.html
# https://habr.com/ru/post/315264/
# https://openweathermap.org/
# https://openweathermap.org/current
