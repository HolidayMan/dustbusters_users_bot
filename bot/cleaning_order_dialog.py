from .bot import bot
from .keyboards import *
import bot.phrases as ph
from .handlers import handle_back_to_menu


@handle_back_to_menu
def handle_cleaning_type(message):
    pass


@handle_back_to_menu
def handle_place_size(message):
    pass


@handle_back_to_menu
def handle_time_range(message):
    pass


@handle_back_to_menu
def handle_cleaning_date(message):
    pass


@handle_back_to_menu
def handle_cleaning_time(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
@handle_back_to_menu
def handle_additional_services(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
@handle_back_to_menu
def handle_need_additional_service(message):
    pass
