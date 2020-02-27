from telebot import types

AUTHORIZE_BUTTON = types.KeyboardButton("Авторизоваться", request_contact=True)
MAKE_CLEANING_ORDER_BUTTON = types.KeyboardButton("Заказать уборку")

CLEANING_WITHOUT_WINDOWS = types.KeyboardButton("Уборка квартиры без помывки окон (150 руб/м²)")
CLEANING_WITH_WINDOWS = types.KeyboardButton("Уборка квартиры с помывкой окон (250 руб/м²)")

BACK_TO_MENU_BUTTON = types.KeyboardButton("Назад")
deleteKeyboard = types.ReplyKeyboardRemove()

AUTHORIZE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
AUTHORIZE_KEYBOARD.add(AUTHORIZE_BUTTON)
MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
MENU_KEYBOARD.add(MAKE_CLEANING_ORDER_BUTTON)

CLEANING_TYPE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
CLEANING_TYPE_KEYBOARD.add(CLEANING_WITHOUT_WINDOWS, CLEANING_WITH_WINDOWS, BACK_TO_MENU_BUTTON)
