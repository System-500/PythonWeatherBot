import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
from telebot import types

bot = telebot.TeleBot('TG key')

@bot.message_handler(commands=['start'])
def welcome(message):
    with open("hi.tgs", "rb") as sticker:
        bot.send_sticker(message.chat.id, sticker)
    
    bot.send_message(message.chat.id, f"Cześć, {message.from_user.first_name}!\n"
                                      f"Jestem <b>{bot.get_me().first_name}</b>, bot, który pokazuje pogodę.\n"
                                      f"(Aby ją sprawdzić, wyślij mi /p)", parse_mode='html')

@bot.message_handler(commands=["p"])
def weather(message):
    msg = bot.send_message(message.chat.id, "W jakim mieście chcesz sprawdzić pogodę?")
    bot.register_next_step_handler(msg, wea)

def wea(message):
    try:
        config_dict = get_default_config()
        config_dict['language'] = 'pl'
        owm = OWM("OWM KEY ", config_dict)
        city = message.text
        mgr = owm.weather_manager()
        wth = mgr.weather_at_place(city).weather
        temp_dict_celsius = wth.temperature('celsius')
        wind = wth.wind()
        
        answer = f"Według moich danych w {city}\n{wth.detailed_status}\n"
        answer += f"Prędkość wiatru: {wind.get('speed', 'brak danych')} m/s\n"
        answer += f"Porywy: {wind.get('gust', 'brak danych')} stopni\n"
        answer += f"Temperatura: {temp_dict_celsius['temp']}°C, waha się od {temp_dict_celsius.get('temp_min', 'brak')}°C do {temp_dict_celsius.get('temp_max', 'brak')}°C.\n"

        if temp_dict_celsius['temp'] <= 0:
            answer += "Zimno ❄️"
        elif temp_dict_celsius['temp'] < 20:
            answer += "Pogoda jest umiarkowana 🌤️"
        else:
            answer += "Gorąco! 🔥"

    except NotFoundError:
        answer = "Nie znaleziono takiego miejsca."
        with open("1.tgs", "rb") as sqs:
            bot.send_sticker(message.chat.id, sqs)
    
    bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types=['text'])
def duhust(message):
    if message.text.lower() == "du":
        msg = bot.send_message(message.chat.id, "Du hast")
        bot.register_next_step_handler(msg, mich)

def mich(message):
    if message.text.lower() == "du hast mich":
        with open("du.webp", "rb") as stf:
            bot.send_sticker(message.chat.id, stf)

bot.polling(none_stop=True)
