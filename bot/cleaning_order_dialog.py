from .bot import bot
from .keyboards import *
import bot.phrases as ph

def handle_cleaning_type(message):
    pass


def handle_place_size(message):
    pass


def handle_time_range(message):
    pass


def handle_cleaning_date(message):
    pass


def handle_cleaning_time(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def handle_need_additional_service(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def handle_additional_sevices(message):
    pass
