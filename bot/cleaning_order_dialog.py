import re
from datetime import datetime, timedelta, time

from bot.bot import bot
from bot.keyboards import *
import bot.phrases as ph
from bot.handlers import handle_back_to_menu, back_to_menu_handler
from bot.models import CleaningOrder
from bot.business_services.utils import (get_keyboards_buttons_text, get_last_db_obj, get_cleaning_type_from_name,
                                         has_message_text, set_state, get_current_state, get_windows_type_from_name,
                                         get_cleaning_class_from_type, get_visit_type_from_name, set_menu_state)
from bot.business_services.promocodes import Promocode
from bot.models import Promocode as PromocodeModel

from .states import States
from bot.business_services.enums import (VisitTypes, CallbacksTexts, VisitNames, CleaningWindowsNames,
    CleaningWindowsTypes, PromocodeTypes)


def get_tomorrow_date() -> datetime:
    one_day = timedelta(days=1, hours=3)
    return datetime.utcnow() + one_day


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_type(message):
    if message.text not in get_keyboards_buttons_text(CLEANING_TYPE_KEYBOARD) or not has_message_text(message):
        bot.register_next_step_handler(message, handle_cleaning_type)
        return bot.send_message(message.chat.id, ph.INVALID_CLEANING_TYPE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(get_cleaning_type_from_name(message.text)).from_instance(order)
    cleaning.save()

    windows_keyboard = build_keyboard_with_prices(WINDOWS_KEYBOARD,
                                                  (cleaning.price_without_windows,
                                                   cleaning.price_with_windows))

    bot.register_next_step_handler(message, handle_cleaning_windows)
    return bot.send_message(message.chat.id, ph.CHOOSE_WINDOWS, parse_mode="HTML", reply_markup=windows_keyboard)


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_cleaning_windows(message):
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    if message.text not in get_keyboards_buttons_text(build_keyboard_with_prices(WINDOWS_KEYBOARD,
                                                                                 (cleaning.price_without_windows,
                                                                                  cleaning.price_with_windows))) \
            or not has_message_text(message):
        bot.register_next_step_handler(message, handle_cleaning_windows)
        return bot.send_message(message.chat.id, ph.INVALID_WINDOWS, parse_mode="HTML")

    cleaning.windows = get_windows_type_from_name(message.text)
    cleaning.save()

    bot.register_next_step_handler(message, handle_place_size)
    return bot.send_message(message.chat.id, ph.ENTER_PLACE_SIZE, parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD)


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_place_size(message):
    if not has_message_text(message):
        bot.register_next_step_handler(message, handle_place_size)
        return bot.send_message(message.chat.id, ph.INVALID_PLACE_SIZE, parse_mode="HTML")

    try:
        size = int(message.text)
        if not 30 <= size <= 300:
            raise ValueError
    except ValueError:
        bot.register_next_step_handler(message, handle_place_size)
        return bot.send_message(message.chat.id, ph.INVALID_PLACE_SIZE, parse_mode="HTML")

    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    cleaning.place_size = size
    cleaning.save()

    keyboard = build_keyboard_with_prices(TIME_RANGE_KEYBOARD, (cleaning.price_day_visit,
                                                                cleaning.price_evening_visit,
                                                                cleaning.price_night_visit))

    bot.register_next_step_handler(message, handle_visit_type)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % cleaning.calc_price(), parse_mode="HTML"),
            bot.send_message(message.chat.id, ph.ENTER_TIME_RANGE, parse_mode="HTML", reply_markup=keyboard))


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_visit_type(message):
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    if message.text not in get_keyboards_buttons_text(
            build_keyboard_with_prices(TIME_RANGE_KEYBOARD, (cleaning.price_day_visit,
                                                             cleaning.price_evening_visit,
                                                             cleaning.price_night_visit))) or not has_message_text(
        message):
        bot.register_next_step_handler(message, handle_visit_type)
        return bot.send_message(message.chat.id, ph.INVALID_TIME_RANGE, parse_mode="HTML")

    cleaning.visit = get_visit_type_from_name(message.text)
    cleaning.save()

    bot.register_next_step_handler(message, handle_cleaning_date)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % cleaning.calc_price(), parse_mode="HTML"),
            bot.send_message(message.chat.id, ph.ENTER_DATE % get_tomorrow_date().strftime("%d.%m.%Y"),
                             parse_mode="HTML", reply_markup=BACK_TO_MENU_KEYBOARD))


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
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    cleaning.visit_date = order_date
    cleaning.save()

    time_to_format = None
    if cleaning.visit == VisitTypes.DAY_VISIT.value:
        time_to_format = "12:00"
    elif cleaning.visit == VisitTypes.EVENING_VISIT.value:
        time_to_format = "17:00"
    elif cleaning.visit == VisitTypes.NIGHT_VISIT.value:
        time_to_format = "04:00"

    bot.register_next_step_handler(message, handle_cleaning_time)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % cleaning.calc_price(), parse_mode="HTML"),
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
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)

    if cleaning.visit == VisitTypes.DAY_VISIT.value:
        if not time(hour=9) <= order_time < time(hour=16):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_DAY, parse_mode="HTML")
    elif cleaning.visit == VisitTypes.EVENING_VISIT.value:
        if not time(hour=16) <= order_time < time(hour=22):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_EVENING, parse_mode="HTML")
    elif cleaning.visit == VisitTypes.NIGHT_VISIT.value:
        if not (time(hour=22) <= order_time <= time(hour=23, minute=59) or time(hour=0) <= order_time <= time(hour=9)):
            bot.register_next_step_handler(message, handle_cleaning_time)
            return bot.send_message(message.chat.id, ph.TIME_MUST_BE_NIGHT, parse_mode="HTML")

    cleaning.visit_time = order_time
    cleaning.save()

    set_state(message.chat.id, States.S_HANDLE_ADDITIONAL_SERVICE.value)
    return (bot.send_message(message.chat.id, ph.SHOW_PRICE % cleaning.calc_price(), parse_mode="HTML",
                             reply_markup=deleteKeyboard),
            bot.send_message(message.chat.id, ph.DO_YOU_NEED_ADDITIONAL_SERVICES,
                             parse_mode="HTML", reply_markup=ADDSERVICE_KEYBOARD))


@bot.callback_query_handler(func=lambda call: get_current_state(
    user_id=call.message.chat.id) == States.S_HANDLE_ADDITIONAL_SERVICE.value
                                              and call.data == YES_ADDSERVICE_BUTTON.callback_data)
def handle_additional_services_yes(call):
    message = call.message
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    message_text, keyboard = build_cleaning_addservices_message_and_keyboard(cleaning)

    return bot.edit_message_text(message_text, message.chat.id, message.message_id, parse_mode="HTML",
                                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: get_current_state(
    user_id=call.message.chat.id) == States.S_HANDLE_ADDITIONAL_SERVICE.value
                                              and (
                                                      call.data == NO_ADDSERVICE_BUTTON.callback_data or call.data == ADDSERVICES_MAKE_ORDER_BUTTON.callback_data))
def handle_additional_services_no(call):
    message = call.message
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    bot.edit_message_text(ph.SHOW_PRICE % cleaning.calc_price(), message.chat.id, message.message_id, parse_mode="HTML")
    bot.register_next_step_handler(message, handle_promocode)
    return bot.send_message(message.chat.id, ph.ENTER_PROMOCODE, parse_mode="HTML", reply_markup=PROMOCODE_HANDLING_KEYBOARD)


@bot.callback_query_handler(func=lambda call: get_current_state(
    user_id=call.message.chat.id) == States.S_HANDLE_ADDITIONAL_SERVICE.value and call.data == ADDSERVICE_BACK_TO_MENU_BUTTON.callback_data)
def handle_additional_services_cancel(call):
    order = get_last_db_obj(model=CleaningOrder, user=call.message.chat)
    order.delete()
    bot.delete_message(call.message.chat.id, call.message.message_id)
    return back_to_menu_handler(call.message)


@bot.callback_query_handler(func=lambda call: get_current_state(
    user_id=call.message.chat.id) == States.S_HANDLE_ADDITIONAL_SERVICE.value
                                              and call.data.split('.')[0] ==
                                              CallbacksTexts.CLEANING_ADDITIONAL_SERVICE_CALLBACK.value.split('.')[0])
def handle_choose_additional_service(call):
    message = call.message
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)

    index = int(call.data.split('.')[1])
    cleaning.additional_services[index].chosen = not cleaning.additional_services[index].chosen
    cleaning.save()

    message_text, keyboard = build_cleaning_addservices_message_and_keyboard(cleaning)
    return bot.edit_message_text(message_text, message.chat.id, message.message_id, parse_mode="HTML",
                                 reply_markup=keyboard)


@handle_back_to_menu(delete=True, model=CleaningOrder)
def handle_promocode(message):
    if message.text == DONT_HAVE_PROMOCODE.text:
        return order_recieved(message)

    if not has_message_text(message) or not PromocodeModel.objects.filter(promocode__iexact=message.text).exists():
        bot.register_next_step_handler(message, handle_promocode)
        return bot.send_message(message.chat.id, ph.NO_SUCH_PROMOCODE_EXISTS, parse_mode="HTML", reply_markup=PROMOCODE_HANDLING_KEYBOARD)

    promocode_instance = PromocodeModel.objects.get(promocode__iexact=message.text)
    promocode = Promocode.from_instance(promocode_instance)
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)
    cleaning.promocode = promocode
    cleaning.save()

    return order_recieved(message)


def order_recieved(message: types.Message):
    order = get_last_db_obj(model=CleaningOrder, user=message.chat)
    cleaning = get_cleaning_class_from_type(order.type).from_instance(order)

    additional_services = "\n".join(f"    {ind}) {service.name}"
                                    for ind, service in enumerate(cleaning.additional_services, start=1) if service.chosen)
    if not additional_services:
        additional_services = "Не выбрано"
    visit = None
    for visit_type in VisitTypes:
        if visit_type.value == cleaning.visit:
            visit = VisitNames[visit_type.name].value

    for windows_type in CleaningWindowsTypes:
        if windows_type.value == cleaning.windows:
            cleaning_type = CleaningWindowsNames[windows_type.name].value

    visit_date = cleaning.visit_date.strftime("%d.%m.%Y")
    visit_time = cleaning.visit_time.strftime("%H:%M")

    cleaning.save_to_amocrm()

    if cleaning.promocode:
        promocode_message = f"Промокод использован: {cleaning.promocode.promocode} ({f'-{cleaning.promocode.amount}%' if cleaning.promocode.promo_type == PromocodeTypes.PERCENT.value else f'-{cleaning.promocode.amount} ₽'})"
    else:
        promocode_message = "Промокод не введен"

    set_menu_state(message.chat.id)
    return bot.send_message(message.chat.id, ph.ORDER_RECIEVED % (cleaning.name,
                                                                  cleaning_type,
                                                                  cleaning.place_size,
                                                                  visit,
                                                                  visit_date,
                                                                  visit_time,
                                                                  additional_services,
                                                                  cleaning.calc_price(),
                                                                  promocode_message),
                            parse_mode="HTML", reply_markup=MENU_KEYBOARD)
