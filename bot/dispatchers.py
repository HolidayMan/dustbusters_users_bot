# from .bot import bot
# from .keyboards import MAKE_CLEANING_ORDER_BUTTON, CLEANING_TYPE_KEYBOARD
# import bot.phrases as ph
from .cleaning_order_dialog import *
from .utils import create_obj
from .models import CleaningOrder


@bot.message_handler(func=lambda message: message.text == MAKE_CLEANING_ORDER_BUTTON.text)  # TODO: pickle can't save locals and pyTelegramBotAPI uses pickle
@create_obj(CleaningOrder)
def make_cleaning_order(message):
    bot.register_next_step_handler(message, handle_cleaning_type)
    return bot.send_message(message.chat.id, ph.WHAT_TYPE_OF_CLEANING, parse_mode="HTML", reply_markup=CLEANING_TYPE_KEYBOARD)
