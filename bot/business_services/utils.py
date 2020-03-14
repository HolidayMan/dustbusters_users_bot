import re
from telebot import types

from vedis import Vedis

from bot.models import TgUser, Contact
from dustbusters_users_bot.settings import STATES_FILE
from bot.states import States
from bot.business_services.cleaning import CLEANINGS, Cleaning
from bot.business_services.enums import CleaningWindows, CleaningWindowsNames, VisitNames, VisitTypes


def user_exists(message) -> bool:
    return TgUser.objects.filter(tg_id=message.chat.id).exists()


def contact_exists(message):
    return Contact.objects.filter(user__tg_id=message.chat.id).exists()


def create_user(message):
    new_user = TgUser(tg_id=message.chat.id)
    if message.chat.username:
        new_user.username = message.chat.username
    if message.chat.first_name:
        new_user.first_name = message.chat.first_name
    new_user.save()


def set_state(user_id, value):
    with Vedis(STATES_FILE) as db:
        try:
            db[user_id] = value
            return True
        except:
            return False


def get_current_state(user_id):
    with Vedis(STATES_FILE) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return States.S_CHOOSE_MENU_OPT.value


def set_menu_state(user_id):
    with Vedis(STATES_FILE) as db:
        try:
            db[user_id] = States.S_CHOOSE_MENU_OPT.value
            return True
        except:
            return False


def get_keyboards_buttons_text(keyboard: types.ReplyKeyboardMarkup):
    return [button['text'] for row in keyboard.keyboard for button in row]


def get_last_db_obj(model, user: types.Chat):
    return model.objects.filter(user=TgUser.objects.get(tg_id=user.id)).order_by("-id")[0]


def create_obj(model):
    def inner(func):
        def wrapper(message, *args, **kwargs):
            new_obj = model(user=TgUser.objects.get(tg_id=message.chat.id))
            new_obj.save()
            return func(message, *args, **kwargs)
        return wrapper
    return inner


def get_cleaning_type_from_name(name: str) -> int:
    return list(filter(lambda cleaning: cleaning.name == name, CLEANINGS.values()))[0].cleaning_type


def get_windows_type_from_name(name: str) -> int:
    pattern_with_windows = CleaningWindowsNames.WITH_WINDOWS.value\
        .replace("(", r"\(").replace(")", r"\)").replace("%s", r"(\d+)")
    pattern_without_windows = CleaningWindowsNames.WITHOUT_WINDOWS.value\
        .replace("(", r"\(").replace(")", r"\)").replace("%s", r"(\d+)")
    if re.match(pattern_with_windows, name):
        return CleaningWindows.WITH_WINDOWS.value
    elif re.match(pattern_without_windows, name):
        return CleaningWindows.WITHOUT_WINDOWS.value
    else:
        raise ValueError(f"such windows type {name} was not found")


def get_visit_type_from_name(name: str) -> int:
    for visit_name in VisitNames:
        pattern = visit_name.value.replace("(", r"\(").replace(")", r"\)").replace("%s", r"(\d+)")
        if re.match(pattern, name):
            return VisitTypes[visit_name.name].value
    raise ValueError(f"such visit type {name} was not found")


def has_message_text(message):
    return bool(message.text)


def get_cleanings_names() -> list:
    return [cleaning.name for cleaning in CLEANINGS.values()]


def get_cleaning_class_from_type(cleaning_type: int) -> Cleaning:
    return CLEANINGS[cleaning_type]
