import telebot
import logging
from dustbusters_users_bot.settings import TOKEN, LOG_FILE


bot = telebot.TeleBot(TOKEN)

logger = telebot.logger
logging.basicConfig(filename=LOG_FILE, filemode='a', format='%(asctime)s:%(name)s - %(message)s')

bot.enable_save_next_step_handlers(delay=1)
bot.load_next_step_handlers()
