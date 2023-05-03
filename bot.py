from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from functions import gpt_func, time_func, quote_func, weather_func, wiki_photo_func, news_func, kitties_func, \
    dogs_func, capybara, actual_crypto_rate, actual_rate, voice_to_txt_func, recipes, email_sending, map_func, traffic, \
    black_white_filter, cambridge_dictionary_func, bored_func, be_like_bill_func, jokes_func, fox_pict_func, \
    numbers_facts, anime
import asyncio
import os
import aiohttp
from data import db_session
from data.user import User

reply_keyboard = [['/help'], ['/GIT'], ['/weather'], ['/time'], ['/phrase_of_the_day'], ['/news'],
                  ['/cambridge_dictionary'], ['/animals'], ['/map'], ['/black_and_white'], ['/economics'], ['/GPT'],
                  ['/cooking'], ['/voice_yt'], ['/voice_to_txt'], ['/RESULT'], ['/email'], ['/random_action'],
                  ['/bill'], ['/jokes'], ['/numbers'], ['/anime']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

reply_keyboard_news = [['/specific_news'], ['/general_news']]
markup_news = ReplyKeyboardMarkup(reply_keyboard_news, one_time_keyboard=True)

reply_keyboard_news_topic = [['/business'], ['/entertainment'], ['/general'], ['/health'], ['/science'], ['/sports'],
                             ['/technology']]
markup_news_topic = ReplyKeyboardMarkup(reply_keyboard_news_topic, one_time_keyboard=True)

btn_loc = KeyboardButton('Отправить геопозицию', request_location=True)
markup_weather_loc = ReplyKeyboardMarkup([[btn_loc]], one_time_keyboard=True)

reply_keyboard_economics = [['/exchange_rate'], ['/crypto_rate']]
markup_economics = ReplyKeyboardMarkup(reply_keyboard_economics, one_time_keyboard=True)

reply_keyboard_bit = [['/BTC'], ['/ETH'], ['/BNB'], ['/LTC'], ['SOL'], ['/DOGE'], ['/ADA'], ['/DOT'], ['/XRP'],
                      ['/LINA']]
markup_bit = ReplyKeyboardMarkup(reply_keyboard_bit, one_time_keyboard=True)

reply_keyboard_exch = [['/USD'], ['/EUR'], ['/CNY'], ['/GBP'], ['/JPY'], ['/CHF'], ['/UAH'], ['/TRY'], ['/AUD'],
                       ['/KZT']]
markup_exch = ReplyKeyboardMarkup(reply_keyboard_exch, one_time_keyboard=True)

reply_keyboard_animals = [['/kitties'], ['/dogs'], ['/capybara'], ['/fox']]
markup_animals = ReplyKeyboardMarkup(reply_keyboard_animals, one_time_keyboard=True)

reply_keyboard_capybara = [['/capybara_random_image'], ['/capybara_random_fact']]
markup_capybara = ReplyKeyboardMarkup(reply_keyboard_capybara, one_time_keyboard=True)

reply_keyboard_bill = [['/bill_name'], ['/bill_text']]
markup_bill = ReplyKeyboardMarkup(reply_keyboard_bill, one_time_keyboard=True)

reply_keyboard_cooking = [['/get_random_recipe'], ['/find_recipe'], ['/find_recipe_id']]
markup_cooking = ReplyKeyboardMarkup(reply_keyboard_cooking, one_time_keyboard=True)

reply_keyboard_lang = [['/RU'], ['/UK'], ['/US'], ['/FR'], ['/DUTCH'], ['/ITA'], ['/SPAN'], ['/DK']]
markup_lang = ReplyKeyboardMarkup(reply_keyboard_lang, one_time_keyboard=True)

reply_keyboard_jokes = [['/geek_jokes'], ['/punch_jokes']]
markup_jokes = ReplyKeyboardMarkup(reply_keyboard_jokes, one_time_keyboard=True)

reply_keyboard_anime = [['/find_anime'], ['/find_anime_id']]
markup_anime = ReplyKeyboardMarkup(reply_keyboard_anime, one_time_keyboard=True)

reply_keyboard_numbers = [['/just_number'], ['/math_number'], ['/date_number']]
markup_numbers = ReplyKeyboardMarkup(reply_keyboard_numbers, one_time_keyboard=True)


###########################################

########################
# numbers

async def numbers_command(update, context):
    await update.message.reply_html(rf"Выберите ниже то, что желаете знать о числах или датах из предложенного!",
                                    reply_markup=markup_numbers)


async def just_number_command(update, context):
    await update.message.reply_text('Введите число')
    return 1


async def just_number_command_resp(update, context):
    func = numbers_facts.get_num([update.message.text])
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)
    return ConversationHandler.END


async def date_number_command(update, context):
    await update.message.reply_text('Введите дату в формате - 01 23 ( где 01 - месяц, 23 - день )')
    return 1


async def date_number_command_resp(update, context):
    func = numbers_facts.get_date(update.message.text.split(' '))
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)
    return ConversationHandler.END


async def math_number_command(update, context):
    await update.message.reply_text('Введите число')
    return 1


async def math_number_command_resp(update, context):
    func = numbers_facts.get_math([update.message.text])
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)
    return ConversationHandler.END


########################
# jokes

async def jokes_command(update, context):
    await update.message.reply_html(rf"Выберите тип шутки из предложенных!", reply_markup=markup_jokes)


async def geek_jokes_command(update, context):
    func = jokes_func.jokes_chak()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def punch_jokes_command(update, context):
    func = jokes_func.jokes_panch()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


########################
# black and white
async def black_and_white_command(update, context):
    await update.message.reply_text(f"Отправьте мне картинку(в виде файла без сжатия) и удивитесь результату")
    return 1


async def downloader_img(update, context):
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('files/image.img')

    answer = black_white_filter.black_white()
    if answer != 'error':
        await context.bot.sendDocument(update.message.chat_id, document=open(answer, 'rb'))
        await update.message.reply_html(rf"Вот!", reply_markup=markup)
        os.remove(answer)
    else:
        await update.message.reply_html(rf"Внимательнее посмотрите какой файл Вы отправляете", reply_markup=markup)

    return ConversationHandler.END


########################
# bill

async def bill(update, context):
    await update.message.reply_html(rf"Функция временно не работает из за ошибок с API", reply_markup=markup)


async def bill_name(update, context):
    func = be_like_bill_func.bill_name(update.message.text)
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def bill_text(update, context):
    func = be_like_bill_func.bill_text(update.message.text)
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


########################
# bored_func
async def get_random_action(update, context):
    func = bored_func.random_event()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


########################
# map
async def map_command(update, context):
    await update.message.reply_html(rf"Поделитесь с нами вашей геолокацией для работы с картой!",
                                    reply_markup=markup_weather_loc)
    return 1


async def map_command_response(update, context):
    long, lang = update.message.location.longitude, update.message.location.latitude

    func0 = traffic.traffic(f'{long},{lang}')
    answer0 = await func0
    await context.bot.send_message(update.message.chat_id, text=answer0)

    func = map_func.get_address_from_coords(f'{long},{lang}')
    answer = await func
    await update.message.reply_html(rf"Ваш адрес: {answer}", reply_markup=markup)

    return ConversationHandler.END


########################
# help
async def help_command(update, context):
    await update.message.reply_text(
        "/weather - выводит погоду по вашему отправленному местоположению"
        "\n\n/time - выводит время самых популярных мест"
        "\n\n/economics - дает возможность посмотреть курсы крипты и валют"
        "\n\n/phrase_of_the_day - выводит фразу дня с картинкой автора ( иногда картинка не находится по причине ее отсутсвия в википедии )"
        "\n\n/news - можете выбрать special news и ввести то, что хотите найти, или выбрать general news и выбрать из предоставленных топиков"
        "\n\n/animals - дает возможность получить милого котенка или собачку"
        "\n\n/exchange_rate - выводит курс популярных валют"
        "\n\n/GIT - ссылка на наш гит"
        "\n\n/cambridge_dictionary - работа с Cambridge Dictionary"
        "\n\n/map - работа с картой"
        "\n\n/black_and_white - работа с изображением(возвращает картинку в черно-белоф формате)"
        "\n\n/GPT - общение с AI от OpenAI"
        "\n\n/voice_yt - по ссылке из ютуб достает звук из видео"
        "\n\n/crypto_rate - из списка можете выбрать интересующую Вас крипту и получить ее курс"
        "\n\n/voice_to_txt - из wav файла достаем звук, преобразуем его потом в текст"
        "\n\n/cooking - с этим вы станете настоящим шеф-поваром, можно запросить рандомный рецепт, найти рецепт по виду блюда, а потом инструкцию к его приготовлению"
        "\n\n/RESULT - давайте посмотрим на кол-во ваших вызовов кнопки start"
        "\n\n/email - позволяет отправить сообщение любому человеку по почте прямо из бота"
        "\n\n/random_action - если вам нечем заняться, запросите у бота рандомное действие"
        "\n\n/bill - будь как Билл"
        "\n\n/jokes - шутки до гроба"
        "\n\n/numbers - интересные факты о числах и не только"
        "\n\n/anime - здесь вы можете найти любое аниме на свой вкус")


########################
# RESULT
async def result_command(update, context):
    usertg = update.effective_user
    id = usertg.id
    db_sess = db_session.create_session()
    person = db_sess.query(User).filter(User.tg_id == id).first()
    await update.message.reply_html(
        rf"Хай, {person.name} или {person.tg_id} - как Вам удобнее. Вот ваш score - {person.count}. Вы, видимо, часто нажимали на /start! ;D",
        reply_markup=markup)


########################
# погода
async def weather_command(update, context):
    await update.message.reply_html(rf"Поделитесь с нами вашей локацией для поиска погоды в вашем районе!",
                                    reply_markup=markup_weather_loc)
    return 1


async def weather_command_response(update, context):
    long, lang = update.message.location.longitude, update.message.location.latitude
    func = weather_func.weather((long, lang))
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)
    return ConversationHandler.END


########################
# новости
async def news_command(update, context):
    await update.message.reply_html(rf"Какие новости вас интересуют?", reply_markup=markup_news)


async def general_news(update, context):
    await update.message.reply_html(rf"Выберите топик", reply_markup=markup_news_topic)


async def business(update, context):
    func = news_func.get_news('business', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def entertainment(update, context):
    func = news_func.get_news('entertainment', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def general(update, context):
    func = news_func.get_news('general', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def health(update, context):
    func = news_func.get_news('health', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def science(update, context):
    func = news_func.get_news('science', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def sports(update, context):
    func = news_func.get_news('sports', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def technology(update, context):
    func = news_func.get_news('technology', 'us')
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def specific_news(update, context):
    await update.message.reply_text("enter the topic you are interested in (for example, Putin)")
    return 1


async def specific_news_response(update, context):
    func = news_func.get_spec_news(update.message.text)
    answer = await func
    await update.message.reply_html(answer, reply_markup=markup)
    return ConversationHandler.END


########################
# фраза дня
async def quote_command(update, context):
    func = quote_func.quote()
    answer = await func
    await update.message.reply_text(f'{answer[0]}')
    await context.bot.send_message(update.message.chat_id, text=answer[1])


########################
# гит
async def git_command(update, context):
    await update.message.reply_text(
        'Вот ссылка на наш гит:\n\nhttps://github.com/Kr0uxx/Web-ProjectXXX\n\nИ на наши профили:\n\nАртем - https://github.com/YL-bot\n\nМаксим - https://github.com/Kr0uxx\n\nКатя - https://github.com/katiarapter')


########################
# время
async def time_command(update, context):
    func = time_func.time()
    answer = await func
    # print(answer)
    await update.message.reply_text(answer)


########################
# chat gpt
async def gpt_command(update, context):
    await update.message.reply_text('Задайте мне вопрос')
    return 1


async def message_answer(update, context):
    txt = update.message.text
    answer = gpt_func.ask(txt, 0)
    await update.message.reply_html(rf"{answer}", reply_markup=markup)
    return ConversationHandler.END


########################
# start
async def start_command(update, context):
    user = update.effective_user
    id = user.id
    db_sess = db_session.create_session()

    person = db_sess.query(User).filter(User.tg_id == id).first()

    if person:
        person.count += 1
        db_sess.commit()
    else:
        usera = User()
        usera.tg_id = id
        usera.name = user.mention_html()
        usera.count = 1
        db_sess.add(usera)
        db_sess.commit()

    await update.message.reply_html(
        rf"Здравствуй, {user.mention_html()}! Я бот с разными функциями, во мне даже есть GPT - можем пообщаться! Давай посмотрим на то, что я еще умею :D - для этого можете вызвать /help",
        reply_markup=markup)


########################
# stop
async def stop(update, context):
    return ConversationHandler.END


#########################
# animals
async def animals_command_response(update, context):
    await update.message.reply_html(rf"Выберите вид животного, картинку которого хотите увидеть",
                                    reply_markup=markup_animals)


# cats
async def kitties_command(update, context):
    func = kitties_func.kitties()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


# dogs
async def dogs_command(update, context):
    func = dogs_func.dogs()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


# fox
async def fox_command(update, context):
    func = fox_pict_func.foxes()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


# capybara
async def capybara_command_response(update, context):
    await update.message.reply_html(rf"Вы хотите увидеть картинку или узнать факт о капибарах?",
                                    reply_markup=markup_capybara)


async def capybara_img(update, context):
    func = capybara.capybara_img()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def capybara_fact(update, context):
    func = capybara.capybara_fact()
    answer = await func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


########################
# anime アニメ
async def anime_response(update, context):
    await update.message.reply_html(rf"find_anime - найти топ самых популярных аниме по названию; "
                                    rf"find_anime_id - найти аниме по id",
                                    reply_markup=markup_anime)


async def anime_find(update, context):
    await update.message.reply_text('Введите ключевое слово для поиска тайтлов (на английском)')
    return 1


async def anime_find_response(update, context):
    func = anime.find_anime(update.message.text)
    answer = await func
    if answer[1] == 1:
        await update.message.reply_html(rf"{answer[0]}", reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(rf"{answer[0]}")


async def anime_id(update, context):
    await update.message.reply_text('Введите id, чтобы узнать подробную информацию о тайтле')
    return 1


async def anime_id_response(update, context):
    func = anime.find_anime_id(update.message.text)
    answer = await func
    if answer[1] == 1:
        await update.message.reply_html(rf"{answer[0]}", reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(rf"{answer[0]}")


########################
# крипта и курс
async def economics_command_response(update, context):
    await update.message.reply_html(rf"Выберите тему, интересующую вас",
                                    reply_markup=markup_economics)


# крипта

async def crypto_rate_command(update, context):
    await update.message.reply_html(rf"Выберите то, что хотите посмотреть", reply_markup=markup_bit)


async def crypto_rate_btc_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('BTC')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_eth_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('ETH')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_bnb_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('BNB')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_ltc_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('LTC')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_sol_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('SOL')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_doge_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('DOGE')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_ada_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('ADA')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_dot_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('DOT')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_xrp_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('XRP')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def crypto_rate_lina_command(update, context):
    func = actual_crypto_rate.get_actual_crypto_rate('LINA')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


# курс
async def exchange_rate_command(update, context):
    await update.message.reply_html(rf"Выберите курс, который вам интересен", reply_markup=markup_exch)


async def exchange_rate_usd_command(update, context):
    func = actual_rate.get_actual_rate('USD')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_eur_command(update, context):
    func = actual_rate.get_actual_rate('EUR')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_cny_command(update, context):
    func = actual_rate.get_actual_rate('CNY')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_gbp_command(update, context):
    func = actual_rate.get_actual_rate('GBP')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_jpy_command(update, context):
    func = actual_rate.get_actual_rate('JPY')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_chf_command(update, context):
    func = actual_rate.get_actual_rate('CHF')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_uah_command(update, context):
    func = actual_rate.get_actual_rate('UAH')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_try_command(update, context):
    func = actual_rate.get_actual_rate('TRY')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_aud_command(update, context):
    func = actual_rate.get_actual_rate('AUD')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


async def exchange_rate_kzt_command(update, context):
    func = actual_rate.get_actual_rate('KZT')
    answer = func
    await update.message.reply_html(rf"{answer}", reply_markup=markup)


########################
# Кулинария, кухня, все дела

async def cooking_command_response(update, context):
    await update.message.reply_html(rf"Что конкретно вы хотите?",
                                    reply_markup=markup_cooking)


async def random_recipe(update, context):
    await update.message.reply_text('''По желанию укажите один или несколько фильтров из доступных через запятую(если не хотите, то введите nothing):
    \n-vegetarian\n-vegan\n-greek\n-italian\n-african\n-american\n-british\n-cajun\n-caribbean\n-chinese\n-eastern european\n-european\n-french\n-german\n-greek\n-indian\n-irish\n-italian\n-japanese\n-jewish\n-korean\n-latin american\n-mediterranean\n-mexican\n-middle eastern\n-nordic\n-southern\n-spanish\n-thai\n-vietnamese''')
    return 1


async def random_recipe_response(update, context):
    func = recipes.get_random_recipe(update.message.text.lower())
    answer = await func
    if answer[1] == 1:
        await update.message.reply_html(rf"{answer[0]}", reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(rf"{answer[0]}")


async def find_recipe(update, context):
    await update.message.reply_text(
        'Введите название типа блюда и количество желаемых рецептов(от 1 до 100, по умолчанию - 30) через пробел')
    return 1


async def find_recipe_response(update, context):
    mess = update.message.text.split()
    func = recipes.find_a_recipe(mess[0], mess[1] if len(mess) > 1 else 30)
    answer = await func
    await update.message.reply_html(answer, reply_markup=markup)
    return ConversationHandler.END


async def recipe_inf(update, context):
    await update.message.reply_text(
        'Введите ID рецепта, чтобы найти его рецепт')
    return 1


async def recipe_inf_response(update, context):
    func = recipes.get_recipe_inf(update.message.text)
    answer = await func
    await update.message.reply_html(answer[0], reply_markup=markup)
    return ConversationHandler.END


#######################
# Cambridge dictionary
async def dictionary_command(update, context):
    await update.message.reply_text(rf'''Please, enter with a space a language(choose from available) and a word(In English): 
-italian
-japanese
-polish
-portuguese
-spanish
-arabic
-catalan
-hindi
-korean
-russian
-turkish
''')
    return 1


async def dictionary_command_response(update, context):
    mess = update.message.text.split()
    mess.append('')
    mess.append('')
    func = cambridge_dictionary_func.get_translate(mess[0].lower(), mess[1].lower())
    answer = await func
    if answer[1] == 1:
        await update.message.reply_html(rf'{answer[0]}', reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text(rf'{answer[0]}')


########################
# перевод звука из ютуб
async def voice_yt_command(update, context):
    await update.message.reply_html(
        rf"Функция работала на момент 21 апреля, потом снова полетела из за обновления ютуб."
        "Не наша вина, но 'pytube' улетел уже в какой раз. Для просмотра самой функции можно в папке"
        "functions найти yt_convert_func.py", reply_markup=markup)


########################
# из wav в текст
async def voice_to_txt_command(update, context):
    await update.message.reply_text(rf"Отправь мне файл в формате WAV")
    return 1


async def downloader(update, context):
    file = await context.bot.get_file(update.message.document)
    await file.download_to_drive('files/main.wav')
    await update.message.reply_html(rf"Выбери язык, который в файле ( если не знаете, то выберите DK )",
                                    reply_markup=markup_lang)
    return ConversationHandler.END


async def voice_dk(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_main()}", reply_markup=markup)


async def voice_ru(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('Russian')}", reply_markup=markup)


async def voice_uk(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('UK English')}", reply_markup=markup)


async def voice_us(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('US English')}", reply_markup=markup)


async def voice_fr(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('French')}", reply_markup=markup)


async def voice_dut(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('Dutch')}", reply_markup=markup)


async def voice_ital(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('Italian')}", reply_markup=markup)


async def voice_sp(update, context):
    await update.message.reply_html(rf"{voice_to_txt_func.voice_lang('Spanish')}", reply_markup=markup)


########################
# отправка по почте
async def email_command(update, context):
    await update.message.reply_text(rf"функция временно отключена")
    return ConversationHandler.END

    #await update.message.reply_text(rf"Отправь мне почту человека и текст письма через точку с запятой (email; text)")
    #return 1


async def email_2_command(update, context):
    user = update.effective_user
    answ = update.message.text.split(';')
    try:
        await update.message.reply_html(rf"временно функция отключена", reply_markup=markup)

        # await update.message.reply_html(rf"{email_sending.send(answ[0], answ[1], str(user.name))}", reply_markup=markup)
    except Exception as e:
        await update.message.reply_html(rf"error, check message again - it must consist from email; text",
                                        reply_markup=markup)
    return ConversationHandler.END


########################
# основа основ основских
def main():
    application = Application.builder().token('6118068525:AAGGfYJ46p8Qe0sYLKC9v8KSsBH7cqybjf4').build()

    # легкие команды
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("GIT", git_command))
    application.add_handler(CommandHandler("time", time_command))
    application.add_handler(CommandHandler("phrase_of_the_day", quote_command))
    application.add_handler(CommandHandler("voice_yt", voice_yt_command))
    application.add_handler(CommandHandler("RESULT", result_command))
    application.add_handler(CommandHandler("random_action", get_random_action))

    # numbers
    application.add_handler(CommandHandler("numbers", numbers_command))

    conv_handler_math_number = ConversationHandler(
        entry_points=[CommandHandler('math_number', math_number_command)],
        states={
            1: [MessageHandler(filters.TEXT, math_number_command_resp)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_math_number)

    conv_handler_date_number = ConversationHandler(
        entry_points=[CommandHandler('date_number', date_number_command)],
        states={
            1: [MessageHandler(filters.TEXT, date_number_command_resp)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_date_number)

    conv_handler_just_number = ConversationHandler(
        entry_points=[CommandHandler('just_number', just_number_command)],
        states={
            1: [MessageHandler(filters.TEXT, just_number_command_resp)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_just_number)

    # jokes
    application.add_handler(CommandHandler("jokes", jokes_command))
    application.add_handler(CommandHandler("geek_jokes", geek_jokes_command))
    application.add_handler(CommandHandler("punch_jokes", punch_jokes_command))

    # bill
    application.add_handler(CommandHandler("bill", bill))
    application.add_handler(CommandHandler("bill_name", bill_name))
    application.add_handler(CommandHandler("bill_text", bill_text))

    # Животные
    application.add_handler(CommandHandler("animals", animals_command_response))
    application.add_handler(CommandHandler("kitties", kitties_command))
    application.add_handler(CommandHandler("dogs", dogs_command))
    application.add_handler(CommandHandler("fox", fox_command))
    application.add_handler(CommandHandler("capybara", capybara_command_response))
    application.add_handler(CommandHandler("capybara_random_image", capybara_img))
    application.add_handler(CommandHandler("capybara_random_fact", capybara_fact))

    # Экономика
    application.add_handler(CommandHandler("economics", economics_command_response))

    # крипта
    application.add_handler(CommandHandler("crypto_rate", crypto_rate_command))

    application.add_handler(CommandHandler("BTC", crypto_rate_btc_command))
    application.add_handler(CommandHandler("ETH", crypto_rate_eth_command))
    application.add_handler(CommandHandler("BNB", crypto_rate_bnb_command))
    application.add_handler(CommandHandler("LTC", crypto_rate_ltc_command))
    application.add_handler(CommandHandler("SOL", crypto_rate_sol_command))
    application.add_handler(CommandHandler("DOGE", crypto_rate_doge_command))
    application.add_handler(CommandHandler("ADA", crypto_rate_ada_command))
    application.add_handler(CommandHandler("DOT", crypto_rate_dot_command))
    application.add_handler(CommandHandler("XRP", crypto_rate_xrp_command))
    application.add_handler(CommandHandler("LINA", crypto_rate_lina_command))

    # курс обычный
    application.add_handler(CommandHandler("exchange_rate", exchange_rate_command))

    application.add_handler(CommandHandler("USD", exchange_rate_usd_command))
    application.add_handler(CommandHandler("EUR", exchange_rate_eur_command))
    application.add_handler(CommandHandler("CNY", exchange_rate_cny_command))
    application.add_handler(CommandHandler("GBP", exchange_rate_gbp_command))
    application.add_handler(CommandHandler("JPY", exchange_rate_jpy_command))
    application.add_handler(CommandHandler("CHF", exchange_rate_chf_command))
    application.add_handler(CommandHandler("UAH", exchange_rate_uah_command))
    application.add_handler(CommandHandler("TRY", exchange_rate_try_command))
    application.add_handler(CommandHandler("AUD", exchange_rate_aud_command))
    application.add_handler(CommandHandler("KZT", exchange_rate_kzt_command))

    # кухня
    application.add_handler(CommandHandler("cooking", cooking_command_response))

    # anime
    application.add_handler(CommandHandler("anime", anime_response))

    # новости
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("general_news", general_news))
    application.add_handler(CommandHandler("business", business))
    application.add_handler(CommandHandler("entertainment", entertainment))
    application.add_handler(CommandHandler("general", general))
    application.add_handler(CommandHandler("health", health))
    application.add_handler(CommandHandler("science", science))
    application.add_handler(CommandHandler("sports", sports))
    application.add_handler(CommandHandler("technology", technology))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('specific_news', specific_news)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, specific_news_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)

    # погода
    conv_handler_weather = ConversationHandler(
        entry_points=[CommandHandler("weather", weather_command)],
        states={
            1: [MessageHandler(filters.LOCATION & ~filters.COMMAND, weather_command_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_weather)

    # файл со звуком wav в текст
    conv_handler_wav = ConversationHandler(
        entry_points=[CommandHandler('voice_to_txt', voice_to_txt_command)],

        states={
            1: [MessageHandler(filters.Document.WAV, downloader)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_wav)

    application.add_handler(CommandHandler("DK", voice_dk))
    application.add_handler(CommandHandler("RU", voice_ru))
    application.add_handler(CommandHandler("UK", voice_uk))
    application.add_handler(CommandHandler("US", voice_us))
    application.add_handler(CommandHandler("FR", voice_fr))
    application.add_handler(CommandHandler("DUTCH", voice_dut))
    application.add_handler(CommandHandler("ITA", voice_ital))
    application.add_handler(CommandHandler("SPAN", voice_sp))

    # GPT
    conv_handler_gpt = ConversationHandler(
        entry_points=[CommandHandler("GPT", gpt_command)],
        states={
            1: [MessageHandler(filters.TEXT, message_answer)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_gpt)

    # email
    conv_handler_email = ConversationHandler(
        entry_points=[CommandHandler("email", email_command)],
        states={
            1: [MessageHandler(filters.TEXT, email_2_command)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_email)

    # КУХНЯ
    # рандомный рецепт
    conv_handler_random_recipe = ConversationHandler(
        entry_points=[CommandHandler("get_random_recipe", random_recipe)],
        states={
            1: [MessageHandler(filters.TEXT, random_recipe_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_random_recipe)

    # поиск рецептов
    conv_handler_find_recipe = ConversationHandler(
        entry_points=[CommandHandler("find_recipe", find_recipe)],
        states={
            1: [MessageHandler(filters.TEXT, find_recipe_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_find_recipe)

    # поиск рецепта по ID
    conv_handler_find_id = ConversationHandler(
        entry_points=[CommandHandler("find_recipe_id", recipe_inf)],
        states={
            1: [MessageHandler(filters.TEXT, recipe_inf_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_find_id)

    # map
    conv_handler_map = ConversationHandler(
        entry_points=[CommandHandler("map", map_command)],
        states={
            1: [MessageHandler(filters.LOCATION & ~filters.COMMAND, map_command_response)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_map)

    # файл со изображение в ЧБ
    conv_handler_black_and_white = ConversationHandler(
        entry_points=[CommandHandler('black_and_white', black_and_white_command)],

        states={
            1: [MessageHandler(filters.Document.ALL, downloader_img)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_black_and_white)

    # cambridge dictionary
    conv_handler_dictionary = ConversationHandler(
        entry_points=[CommandHandler('cambridge_dictionary', dictionary_command)],

        states={
            1: [MessageHandler(filters.TEXT, dictionary_command_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_dictionary)

    # anime

    # поиск аниме по названию
    conv_handler_anime_find = ConversationHandler(
        entry_points=[CommandHandler('find_anime', anime_find)],

        states={
            1: [MessageHandler(filters.TEXT, anime_find_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_anime_find)

    # поиск аниме по id
    conv_handler_anime_id = ConversationHandler(
        entry_points=[CommandHandler('find_anime_id', anime_id)],

        states={
            1: [MessageHandler(filters.TEXT, anime_id_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler_anime_id)

    application.run_polling()


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
