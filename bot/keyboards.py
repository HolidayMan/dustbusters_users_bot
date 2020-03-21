from telebot import types
from typing import Tuple


from bot.business_services.utils import get_cleanings_names
from bot.business_services.enums import VisitPriceNames, CleaningWindowsPriceNames, CallbacksTexts
from bot.business_services.cleaning import Cleaning
from bot import phrases as ph

AUTHORIZE_BUTTON = types.KeyboardButton("Авторизоваться", request_contact=True)
MAKE_CLEANING_ORDER_BUTTON = types.KeyboardButton("Заказать уборку")

WITHOUT_WINDOWS_BUTTON = types.KeyboardButton(CleaningWindowsPriceNames.WITHOUT_WINDOWS.value)
WITH_WINDOWS_BUTTON = types.KeyboardButton(CleaningWindowsPriceNames.WITH_WINDOWS.value)

SOFT_CLEANING_BUTTON = types.KeyboardButton("Уборка квартиры без помывки окон (%s руб/м²)")

DAY_VISIT_BUTTON = types.KeyboardButton(VisitPriceNames.DAY_VISIT.value)
EVENING_VISIT_BUTTON = types.KeyboardButton(VisitPriceNames.EVENING_VISIT.value)
NIGHT_VISIT_BUTTON = types.KeyboardButton(VisitPriceNames.NIGHT_VISIT.value)

YES_ADDSERVICE_BUTTON = types.InlineKeyboardButton("Да✅", callback_data=CallbacksTexts.ADDITIONAL_SERVICE_ACCEPTED.value)
NO_ADDSERVICE_BUTTON = types.InlineKeyboardButton("Нет🚫", callback_data=CallbacksTexts.ADDITIONAL_SERVICE_DECLINED.value)
ADDSERVICE_BACK_TO_MENU_BUTTON = types.InlineKeyboardButton("❌", callback_data=CallbacksTexts.CLEANING_CANCEL.value)
ADDSERVICES_MAKE_ORDER_BUTTON = types.InlineKeyboardButton("Заказать", callback_data=CallbacksTexts.ADDITIONAL_SERVICE_CHOSED.value)

BACK_TO_MENU_BUTTON = types.KeyboardButton("Назад в меню")
deleteKeyboard = types.ReplyKeyboardRemove()

DONT_HAVE_PROMOCODE = types.KeyboardButton("У меня нет промокода")

BACK_TO_MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
BACK_TO_MENU_KEYBOARD.add(BACK_TO_MENU_BUTTON)

AUTHORIZE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
AUTHORIZE_KEYBOARD.add(AUTHORIZE_BUTTON)
MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
MENU_KEYBOARD.add(MAKE_CLEANING_ORDER_BUTTON)

CLEANING_TYPE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
CLEANING_TYPE_KEYBOARD.add(*get_cleanings_names(), BACK_TO_MENU_BUTTON)

WINDOWS_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
WINDOWS_KEYBOARD.add(WITHOUT_WINDOWS_BUTTON, WITH_WINDOWS_BUTTON, BACK_TO_MENU_BUTTON)

PLACE_SIZE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
PLACE_SIZE_KEYBOARD.add(BACK_TO_MENU_BUTTON)

TIME_RANGE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
TIME_RANGE_KEYBOARD.add(DAY_VISIT_BUTTON, EVENING_VISIT_BUTTON, NIGHT_VISIT_BUTTON, BACK_TO_MENU_BUTTON)

ADDSERVICE_KEYBOARD = types.InlineKeyboardMarkup(row_width=2)
ADDSERVICE_KEYBOARD.add(YES_ADDSERVICE_BUTTON, NO_ADDSERVICE_BUTTON, ADDSERVICE_BACK_TO_MENU_BUTTON)

PROMOCODE_HANDLING_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
PROMOCODE_HANDLING_KEYBOARD.add(DONT_HAVE_PROMOCODE, BACK_TO_MENU_BUTTON)


def build_keyboard_with_prices(keyboard, prices):
    buttons = [types.KeyboardButton(json[0]['text']) for json in keyboard.keyboard]
    changed_buttons = [types.KeyboardButton(button.text % price) for button, price in zip(buttons, prices)]
    other_buttons = buttons[len(changed_buttons):]
    new_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=keyboard.resize_keyboard,
                                             one_time_keyboard=keyboard.one_time_keyboard,
                                             selective=keyboard.selective,
                                             row_width=keyboard.row_width)
    new_keyboard.add(*changed_buttons, *other_buttons)

    return new_keyboard


def build_cleaning_addservices_message_and_keyboard(cleaning: Cleaning) -> Tuple[str, types.InlineKeyboardMarkup]:
    message = ""
    message += ph.CHOOSE_ADDITIONAL_SERVICES
    message += "\n\n"

    for index, service in enumerate(cleaning.additional_services, start=1):
        message += f"<b>{index}. {service.build_name()}</b> {'✅' if service.chosen else ''}\n"

    message += "\n"
    message += ph.SHOW_PRICE % cleaning.calc_price()

    keyboard = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for index, service in enumerate(cleaning.additional_services):
        if service.chosen:
            button_text = f"{index+1}✅"
        else:
            button_text = str(index+1)
        button_callback = CallbacksTexts.CLEANING_ADDITIONAL_SERVICE_CALLBACK.value % index
        button = types.InlineKeyboardButton(button_text, callback_data=button_callback)
        buttons.append(button)

    keyboard.add(*buttons)
    keyboard.row(ADDSERVICES_MAKE_ORDER_BUTTON, ADDSERVICE_BACK_TO_MENU_BUTTON)

    return message, keyboard
