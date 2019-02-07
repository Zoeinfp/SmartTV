import json
import random

import requests
from google.cloud import translate

from sogetv_app.models import ImageData, MessageData, EventData, WeatherData, db


def create_new_message(new_message):
    """
    Create message
    :param new_message:
    """
    get_or_create_message_data(message_to_store=new_message)


def save_image(image_string):
    """
    Save image
    :param image_string: Image converted in Bytes
    :return: True boolean
    """
    new_image = ImageData(image_string=image_string)
    db.session.add(new_image)
    db.session.commit()
    return True


def get_or_create_message_data(message_to_store):
    """
    Get or create message
    :param message_to_store: Message to store
    :return: Message to store
    """
    exists = db.session.query(MessageData.id).filter_by(message=message_to_store).scalar() is not None

    if exists:
        return db.session.query(MessageData).filter_by(message=message_to_store).first()
    else:
        new_message_obj = MessageData(message=message_to_store)
        db.session.add(new_message_obj)
        db.session.commit()
        return message_to_store


def get_or_create_event(title, description=None, start=None, end=None):
    """
    Get or create event
    :param title: Event title
    :param description: Event description
    :param start: Event start date
    :param end: Event end date
    :return: Event
    """
    exists = db.session.query(EventData.id).filter_by(title=title).scalar() is not None
    print('Create a new event')
    if exists:
        print("Exist!...")
        return db.session.query(EventData).filter_by(title=title).first()
    else:
        if title and description and start and end:
            print("....Weird")
            new_event_obj = EventData(title=title, description=description, start=start, end=end)
        elif title and start and end:
            print('Creating...')
            new_event_obj = EventData(title=title, start=start, end=end)
        else:
            print('Does not work...')
            new_event_obj = EventData(title=title, start=start)

        db.session.add(new_event_obj)
        db.session.commit()
        return new_event_obj


def create_weather_data(new_city):
    """
    Create weather data
    :param new_city: Requested city
    :return: name
    """
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=254d0bd84bee0354b5b34e17f870cf04'

    r = requests.get(url.format(new_city)).json()

    name = new_city
    temperature = r['main']['temp']
    description = r['weather'][0]['description'],
    icon = r['weather'][0]['icon'],
    print(new_city)
    get_or_create_weather_data(name=name, temperature=temperature, description=description[0], icon=icon[0])
    return name


def get_or_create_weather_data(name, temperature, description, icon):
    """
    Get or create weather data
    :param name: name of the city
    :param temperature: temperature for the city
    :param description: description of weather for the city
    :param icon: image for the city's weather
    :return: name
    """
    exists = db.session.query(WeatherData.id).filter_by(name=name).scalar() is not None

    if exists:
        return db.session.query(WeatherData).filter_by(name=name).first()
    else:
        new_weather_obj = WeatherData(name=name, temperature=temperature, description=description, icon=icon)
        db.session.add(new_weather_obj)
        db.session.commit()
        return name


def zodiac():
    """
    Zodiac method
    :return: Array of zodiac data
    """
    signs = ['capricorn',
             'aquarius',
             'pisces',
             'aries',
             'taurus',
             'gemini',
             'cancer',
             'leo',
             'virgo',
             'libra',
             'scorpio',
             'sagittarius']

    sign = random.choice(signs)
    day = ('day', 'today')
    response = requests.post('https://aztro.sameerkumar.website/', params=(('sign', sign), day))
    text = json.loads(response.text)
    mood = text['mood']
    lucky_time = text['lucky_time']
    description = text['description']

    client = translate.Client()
    mood_fr = client.translate(mood, source_language='en', target_language='fr')
    lucky_time_fr = client.translate(lucky_time, source_language='en', target_language='fr')
    description_fr = client.translate(description, source_language='en', target_language='fr')
    sign_fr = client.translate(sign, source_language='en', target_language='fr')

    return [sign, sign_fr['translatedText'],
            mood, mood_fr['translatedText'],
            lucky_time, lucky_time_fr['translatedText'],
            description, description_fr['translatedText']]
