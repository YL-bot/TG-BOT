import requests
from bs4 import BeautifulSoup

link = "https://bitinfocharts.com/ru/crypto-kurs/"
r = requests.get(link)
soup = BeautifulSoup(r.text, "html.parser")
listt = soup.find('tbody').text[2::].split('    ')

# вся криптовалюта, доступная пользователю, если добавлять крипту в бота, то также добавить в этот список:
currencies_list = ["BTC", "ETH", "BNB", "LTC", "SOL", "DOGE", "ADA", "DOT", "XRP", "LINA"]
currencies_names = []

# создание списка с курсами нужных валют
for i in listt:
    if i.split()[0] in currencies_list:
        currencies_names.append(i.split()[:(i.split().index('$')) + 2])


# функция, возвращающая актуальный курс для нужной криптовалюты
def get_actual_crypto_rate(input_currency):
    rate = 0
    currency = ''
    for name in currencies_names:
        if name[0] == input_currency:
            for j in name[1:name.index('$')]:
                currency += j + ' '
            currency = currency.rstrip()
            rate = name[-1]
    return f'Курс для 1 {currency} составляет {rate} $'
