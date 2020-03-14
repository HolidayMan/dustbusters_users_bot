from telebot import types
from bot.business_services.utils import get_cleanings_names
from bot.business_services.enums import VisitNames, CleaningWindowsNames

AUTHORIZE_BUTTON = types.KeyboardButton("Авторизоваться", request_contact=True)
MAKE_CLEANING_ORDER_BUTTON = types.KeyboardButton("Заказать уборку")

WITHOUT_WINDOWS_BUTTON = types.KeyboardButton(CleaningWindowsNames.WITHOUT_WINDOWS.value)
WITH_WINDOWS_BUTTON = types.KeyboardButton(CleaningWindowsNames.WITH_WINDOWS.value)

SOFT_CLEANING_BUTTON = types.KeyboardButton("Уборка квартиры без помывки окон (%s руб/м²)")

DAY_VISIT_BUTTON = types.KeyboardButton(VisitNames.DAY_VISIT.value)
EVENING_VISIT_BUTTON = types.KeyboardButton(VisitNames.EVENING_VISIT.value)
NIGHT_VISIT_BUTTON = types.KeyboardButton(VisitNames.NIGHT_VISIT.value)

YES_ADDSERVICE_BUTTON = types.InlineKeyboardButton("Да✅", callback_data="additional_service_accepted")
NO_ADDSERVICE_BUTTON = types.InlineKeyboardButton("Нет🚫", callback_data="additional_service_declined")
ADDSERVICE_BACK_TO_MENU_BUTTON = types.InlineKeyboardButton("❌", callback_data="cleaning_cancel")

BACK_TO_MENU_BUTTON = types.KeyboardButton("Назад")
deleteKeyboard = types.ReplyKeyboardRemove()

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
