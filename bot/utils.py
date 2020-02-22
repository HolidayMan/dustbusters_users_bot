from vedis import Vedis

from .models import TgUser, Contact
from dustbusters_users_bot.settings import STATES_FILE
from .states import States


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
