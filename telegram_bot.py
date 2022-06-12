from asyncio.windows_events import INFINITE
from click import command
import telebot
import os
import time
from yaml import load
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

print(API_KEY)
bot = telebot.TeleBot(API_KEY)
bot.config['api_key'] = API_KEY
for i in range(10):
    bot.send_message("-1001778640424", i)
bot.poll()