import requests
from bs4 import BeautifulSoup
import asyncio

# список языков, для которых код страницы отдельный, а соответсвенно нужно парсить каждую по отдельности
incorrect_languages = ['dutch', 'french', 'german', 'indonesian', 'norwegian', 'czech', 'danish', 'malaysian', 'thai,'
                                                                                                               'turkish',
                       'vietnamese', 'chinese-traditional', 'chinese-simplified']
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}


# получение soup, в функцию передаются язык(на выбор пользователя) и слово(пользователь вводит)
def get_url(language, word):
    url = f'https://dictionary.cambridge.org/dictionary/english-{language.lower()}/{word}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # тут if else, потому что при поиске несуществующего слова, ошибки не выкидывает, а перекидывает на главную страницу

    if soup.find('h1').text == '404. Page not found.' or language in incorrect_languages:
        return 'Неверно введен язык, пожалуйста, введите его заново'

    elif soup.find('h1').text[:7] == 'English':
        return 'Такого слова не существует, либо оно отсутствует в словаре, пожалуйста, введите новое слово'

    return soup


def make_html(string):
    answer = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>\n"""
    answer += f'{string}\n'
    answer += """</body>
</html>"""
    return BeautifulSoup(answer, "html.parser")


# функция, которая выдает определения и перевод слова на нужном языке и части речи
async def get_translate(language, word):
    soup = get_url(language, word)
    text = word + '\n\n'
    try:
        for i in soup.find_all('div', class_='pr entry-body__el'):
            arr_full = (list(filter(lambda x: x != '' and x != ' ' and x != '       '
                                              and x != 'Your browser doesn\'t support HTML5 audio',
                                    i)))
            current_pos = make_html(arr_full)

            pos = current_pos.find('span', class_='pos dpos').text  # определение части речи

            # добавление всех значений
            all_meanings = []
            for j in current_pos.find_all('div', class_='ddef_h'):
                all_meanings.append(j.text.strip())

            # добавление всех переводов
            all_translations = []
            for j in current_pos.find_all('span', class_='trans dtrans dtrans-se'):
                all_translations.append(j.text.strip())

            # добавление в ответ
            text += f'{pos}\n' \
                    f'_________________________________________________________\n'
            for j in range(len(all_meanings)):
                text += f'{j + 1})\n' \
                        f'Meaning: {all_meanings[j]}\n\n' \
                        f'Translation: {all_translations[j]}\n\n'
        return text, 1
    except:
        return soup, 0

# print(asyncio.run(get_translate('chinese-traditional', 'run')))
