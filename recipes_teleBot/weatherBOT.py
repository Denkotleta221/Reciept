import telebot
from telebot import types
import requests
import json

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN, API_WEATHER

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Приветствую в прогнозе погоды!\nНапишыте название города")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_WEATHER}&units=metric')
    data = json.loads(res.text)
    if res.status_code == 200:
        clear = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        bot.reply_to(message, f"Погода: {clear}\nТемпература {temp}℃")
    else:
        bot.reply_to(message, "Город указан не верно")

bot.polling(non_stop=True)