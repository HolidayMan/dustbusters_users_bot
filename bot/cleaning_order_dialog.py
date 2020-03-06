from datetime import datetime, timedelta

from .bot import bot
from .keyboards import *
import bot.phrases as ph
from .handlers import handle_back_to_menu
from .models import CleaningOrder
from .utils import get_keyboards_buttons_text, get_last_db_obj, get_trip_type_from_name, has_message_text


def get_tomorrow_date() -> datetime:
    one_day = timedelta(days=1)
    return datetime.utcnow() + one_day


# @check_message_text(ph.INVALID_CLEANING_TYPE, check=lambda t: t in get_keyboards_buttons_text(CLEANING_TYPE_KEYBOARD))
@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_type(message):
    if message.text not in get_keyboards_buttons_text(CLEANING_TYPE_KEYBOARD) or not has_message_text(message):
        bot.register_next_step_handler(message, handle_cleaning_type)
        return bot.send_message(message.chat.id, ph.INVALID_CLEANING_TYPE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    order.type = get_trip_type_from_name(message.text)
    order.save()

    bot.register_next_step_handler(message, handle_place_size)
    return bot.send_message(message.chat.id, ph.ENTER_PLACE_SIZE, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_place_size(message):
    if not has_message_text(message):
        bot.register_next_step_handler(message, handle_place_size)
        return bot.send_message(message.chat.id, ph.INVALID_PLACE_SIZE, parse_mode="HTML")

    try:
        size = int(message.text)
        if size > 1500:  # size is too big
            raise ValueError
    except ValueError:
        bot.register_next_step_handler(message, handle_place_size)
        return bot.send_message(message.chat.id, ph.INVALID_PLACE_SIZE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    order.square_metres = size
    order.save()

    bot.register_next_step_handler(message, handle_time_range)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % order.calc_price(), parse_mode="HTML"),
            bot.send_message(message.chat.id, ph.ENTER_TIME_RANGE, parse_mode="HTML", reply_markup=TIME_RANGE_KEYBOARD))


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_time_range(message):
    if message.text not in get_keyboards_buttons_text(TIME_RANGE_KEYBOARD) or not has_message_text(message):
        bot.register_next_step_handler(message, handle_time_range)
        return bot.send_message(message.chat.id, ph.INVALID_TIME_RANGE, parse_mode="HTML")
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    order.trip = CleaningOrder.get_trip_type(message.text)
    order.save()
    bot.register_next_step_handler(message, handle_cleaning_date)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % order.calc_price(), parse_mode="HTML"),
            bot.send_message(message.chat.id, ph.ENTER_DATE % get_tomorrow_date().strftime("%d.%m.%Y"), parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD))


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
