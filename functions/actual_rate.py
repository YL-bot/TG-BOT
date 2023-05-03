import requests
from bs4 import BeautifulSoup
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

link = "https://www.cbr.ru/currency_base/daily/"
r = requests.get(link)

soup = BeautifulSoup(r.text, "html.parser")
listt = soup.find('tbody').text.split("\n\n")
currencies_names = []
for i in listt[2::]:
    currencies_names.append(i.split("\n")[2::])


# функция для корректировки формы слов у названия валюты в родительный падеж, единственное число,
# чтобы пользователю было максимально комфортно
def correct_currency_form(currency_name):
    if currency_name == "Турецких лир":
        return "турецкой лиры"
    if currency_name == "Казахстанских тенге":
        return "казахстанского тенге"
    currency_name = currency_name.split()
    if len(currency_name) == 1:
        return morph.parse(currency_name[0])[0].inflect({'sing', 'gent'}).word
    elif len(currency_name) > 1 and morph.parse(currency_name[0])[0].tag.POS != 'NOUN':
        return morph.parse(currency_name[0])[0]. \
            inflect({'sing', 'gent', morph.parse(currency_name[1])[0].tag.gender}).word + ' ' + \
            morph.parse(currency_name[1])[0].inflect({'sing', 'gent'}).word
    else:
        string = ''
        for j in currency_name[1::]:
            string += j + ' '
        return morph.parse(currency_name[0])[0].inflect({'sing', 'gent'}).word + ' ' + \
            string.rstrip()


# функция, возвращающая актуальный курс валюты на выбор(передается буквенное сокращение валюты)
def get_actual_rate(input_currency):
    rate = 0
    currency = ''
    for name in currencies_names[:-1]:
        if name[0] == input_currency:
            currency = name[2]
            rate = float(name[3].replace(',', '.')) / float(name[1].replace(',', '.'))
    return f"Курс для 1 {correct_currency_form(currency)} составляет {rate} RUB."

# print(get_actual_rate('USD'))
