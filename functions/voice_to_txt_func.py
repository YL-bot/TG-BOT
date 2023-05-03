import speech_recognition as sr
import os


# надо будет передать язык
# файл будет лежать в папке files под название !   wav_file.wav  !
# но его нужно создать еще будет

# написать форматирование из разных форматов в wav

def voice(lang):
    try:
        lang_dict = {'Russian': 'ru-RU',
                     'UK English': 'en-GB',
                     'US English': 'en-US',
                     'French': 'fr-CA',
                     'Dutch': 'de-DE',
                     'Italian': 'it-IT',
                     'Spanish': 'es-ES'}

        voice = sr.Recognizer()
        with sr.AudioFile('files/main.wav') as source:
            audio_text = voice.listen(source)
            text = voice.recognize_google(audio_text, language=lang_dict[lang])

            return text

    except Exception as e:
        return 'error'


def voice_main():
    languages = ['Russian', 'UK English', 'US English', 'French', 'Dutch', 'Italian', 'Spanish']

    for i in languages:
        txt = voice(i)

        if txt != 'error':
            if txt != '':
                return txt
            else:
                return 'Opssss, seems to be empty... :('

    return 'error'


def voice_lang(lang):
    languages = ['Russian', 'UK English', 'US English', 'French', 'Dutch', 'Italian', 'Spanish']

    return voice(lang)
