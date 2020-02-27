from .bot import bot
from .keyboards import *
import bot.phrases as ph
from .handlers import handle_back_to_menu
from .models import CleaningOrder
from .utils import get_keyboards_buttons_text, get_last_db_obj, get_trip_type_from_name


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_type(message):
    if message.text not in get_keyboards_buttons_text(CLEANING_TYPE_KEYBOARD):
        bot.register_next_step_handler(message, handle_cleaning_type)
        return bot.send_message(message.chat.id, ph.INVALID_CLEANING_TYPE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    order.type = get_trip_type_from_name(message.text)
    order.save()

    bot.register_next_step_handler(message, handle_place_size)
    return bot.send_message(message.chat.id, ph.ENTER_PLACE_SIZE, parse_mode="HTML", reply_markup=deleteKeyboard)


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
