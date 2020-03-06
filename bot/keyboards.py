from telebot import types

AUTHORIZE_BUTTON = types.KeyboardButton("Авторизоваться", request_contact=True)
MAKE_CLEANING_ORDER_BUTTON = types.KeyboardButton("Заказать уборку")

CLEANING_WITHOUT_WINDOWS = types.KeyboardButton("Уборка квартиры без помывки окон (150 руб/м²)")
CLEANING_WITH_WINDOWS = types.KeyboardButton("Уборка квартиры с помывкой окон (250 руб/м²)")

DAY_TRIP_BUTTON = types.KeyboardButton("Дневной выезд 9:00 — 15:00 (0 ₽)")
EVENING_TRIP_BUTTON = types.KeyboardButton("Вечерний выезд 16:00 — 21:00 (1000 ₽)")
NIGHT_TRIP_BUTTON = types.KeyboardButton("Ночной выезд 22:00 — 8:00 (2000 ₽)")

BACK_TO_MENU_BUTTON = types.KeyboardButton("Назад")
deleteKeyboard = types.ReplyKeyboardRemove()

AUTHORIZE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
AUTHORIZE_KEYBOARD.add(AUTHORIZE_BUTTON)
MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
MENU_KEYBOARD.add(MAKE_CLEANING_ORDER_BUTTON)

CLEANING_TYPE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
CLEANING_TYPE_KEYBOARD.add(CLEANING_WITHOUT_WINDOWS, CLEANING_WITH_WINDOWS, BACK_TO_MENU_BUTTON)

PLACE_SIZE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
PLACE_SIZE_KEYBOARD.add(BACK_TO_MENU_BUTTON)

TIME_RANGE_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
TIME_RANGE_KEYBOARD.add(DAY_TRIP_BUTTON, EVENING_TRIP_BUTTON, NIGHT_TRIP_BUTTON, BACK_TO_MENU_BUTTON)

BACK_TO_MENU_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
BACK_TO_MENU_KEYBOARD.add(BACK_TO_MENU_BUTTON)
