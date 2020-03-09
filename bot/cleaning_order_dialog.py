import re
from datetime import datetime, timedelta, time

from .bot import bot
from .keyboards import *
import bot.phrases as ph
from .handlers import handle_back_to_menu, back_to_menu_handler
from .models import CleaningOrder
from .utils import (get_keyboards_buttons_text, get_last_db_obj, get_trip_type_from_name,
                    has_message_text, set_state, set_menu_state, get_current_state)
from .states import States


def get_tomorrow_date() -> datetime:
    one_day = timedelta(days=1, hours=3)
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


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_date(message):
    pattern = r'^(0[1-9]|[1-2][0-9]|3[0-1])\.(0[1-9]|[1-2][0-2])\.2\d\d\d$'
    if not has_message_text(message) or not re.match(pattern, message.text):
        bot.register_next_step_handler(message, handle_cleaning_date)
        return bot.send_message(message.chat.id, ph.INVALID_DATE, parse_mode="HTML")

    order_date = datetime.strptime(message.text, "%d.%m.%Y").date()
    today = (datetime.utcnow() + timedelta(hours=3)).date()

    if not today <= order_date:
        bot.register_next_step_handler(message, handle_cleaning_date)
        return bot.send_message(message.chat.id, ph.PAST_DATE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    order.date = order_date
    order.save()

    if order.trip == CleaningOrder.DAY_TRIP:
        time_to_format = "12:00"
    elif order.trip == CleaningOrder.EVENING_TRIP:
        time_to_format = "17:00"
    elif order.trip == CleaningOrder.NIGHT_TRIP:
        time_to_format = "04:00"

    bot.register_next_step_handler(message, handle_cleaning_time)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % order.calc_price(), parse_mode="HTML"),
            bot.send_message(message.chat.id, ph.ENTER_TIME % time_to_format,
                             parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD))


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_time(message):
    pattern = r"([0-1]*[0-9]|2[0-3]):([0-5][0-9])"
    if not has_message_text(message) or not re.match(pattern, message.text):
        bot.register_next_step_handler(message, handle_cleaning_time)
        return bot.send_message(message.chat.id, ph.INVALID_TIME, parse_mode="HTML")

    order_time = datetime.strptime(message.text, "%H:%M").time()

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)

    if order.trip == CleaningOrder.DAY_TRIP:
        if not time(hour=9) <= order_time < time(hour=16):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_DAY, parse_mode="HTML")
    elif order.trip == CleaningOrder.EVENING_TRIP:
        if not time(hour=16) <= order_time < time(hour=22):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_EVENING, parse_mode="HTML")
    elif order.trip == CleaningOrder.NIGHT_TRIP:
        if not (time(hour=22) <= order_time <= time(hour=23, minute=59) or time(hour=0) <= order_time <= time(hour=9)):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_NIGHT, parse_mode="HTML")

    order.time = order_time
    order.save()

    set_state(message.chat.id, States.S_HANDLE_ADDITIONAL_SERVICE)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % order.calc_price(), parse_mode="HTML", reply_markup=deleteKeyboard),
            bot.send_message(message.chat.id, ph.CHOOSE_ADDITIONAL_SERVICE,
                             parse_mode="HTML", reply_markup=ADDSERVICE_KEYBOARD))


@bot.callback_query_handler(func=lambda call: get_current_state(user_id=call.message.chat.id) and call.data == YES_ADDSERVICE_BUTTON.callback_data)
def handle_additional_services_yes(call):
    pass


@bot.callback_query_handler(func=lambda call: get_current_state(user_id=call.message.chat.id) and call.data == NO_ADDSERVICE_BUTTON.callback_data)
def handle_additional_services_no(call):
    pass


@bot.callback_query_handler(func=lambda call: get_current_state(user_id=call.message.chat.id) and call.data == ADDSERVICE_BACK_TO_MENU_BUTTON.callback_data)
def handle_additional_services_cancel(call):
    order = get_last_db_obj(model=CleaningOrder, user=call.message.chat)
    order.delete()
    bot.delete_message(call.message.chat.id, call.message.message_id)
    return back_to_menu_handler(call.message)


@bot.callback_query_handler(func=lambda call: True)
@handle_back_to_menu
def handle_need_additional_service(message):
    pass
