#!/usr/bin/env python
# coding: utf-8


import random
import nltk
import requests
import config

f = open('bot_config.txt', encoding='utf-8')
BOT_CONFIG = eval(f.read())
api_url = config.APIURL


def clear_phrase(phrase):
    phrase = phrase.lower()

    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- '
    result = ''.join(symbol for symbol in phrase if symbol in alphabet)

    return result


def classify_intent(replica):
    # TODO use ML!

    replica = clear_phrase(replica)

    for intent, intent_data in BOT_CONFIG['intents'].items():
        for example in intent_data['examples']:
            example = clear_phrase(example)

            distance = nltk.edit_distance(replica, example)
            if distance / len(example) < 0.4:
                return intent


def get_answer_by_intent(intent):
    if intent in BOT_CONFIG['intents']:
        responses = BOT_CONFIG['intents'][intent]['responses']
        return random.choice(responses)


def generate_answer(replica):
    # TODO на 3й день
    return


def get_failure_phrase():
    failure_phrases = BOT_CONFIG['failure_phrases']
    return random.choice(failure_phrases)


def weather(city):
    params = {
        'q': city,
        'appid': config.APPID,
        'units': 'metric'
    }
    res = requests.get(api_url, params=params)
    data = res.json()
    return data


def bot(replica):
    # NLU
    intent = classify_intent(replica)

    # Answer generation
    """
    1. Добавила в бот конфиг интент "weather" 
    2. Подключила API сервиса, который сообщает погоду (URL и ключ записала
    в файл "config.py")
    3. Реализовала запись ответа пользователя (а именно город, который передала в функцию запроса погоды)
    4. Сформировала ответ
    5. Очень интересный интенсив, спасибо :)
    """
    if intent == 'weather':
        inp_city = input('Напишите название города, в котором хотите узнать погоду\n')
        res = weather(inp_city)
        template = 'Температура в городе {} составляет {} градусов'
        return template.format(inp_city, res['main']['temp'])
    # выбор заготовленной реплики

    if intent:
        answer = get_answer_by_intent(intent)
        if answer:
            return answer

    # вызов генеративной модели
    answer = generate_answer(replica)
    if answer:
        return answer

    # берем заглушку
    return get_failure_phrase()


print(bot('Погода'))
