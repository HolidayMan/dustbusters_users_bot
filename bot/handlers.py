from .bot import bot
import bot.phrases as ph
from bot.business_services.utils import set_menu_state, get_last_db_obj
from .keyboards import BACK_TO_MENU_BUTTON, MENU_KEYBOARD


def handle_back_to_menu(delete=False, model=None):
    def inner(func):
        def wrapper(message, *args, **kwargs):
            if message.text == BACK_TO_MENU_BUTTON.text:
                if delete:
                    obj = get_last_db_obj(model, message.chat)
                    obj.delete()
                return back_to_menu_handler(message)
            else:
                return func(message, *args, **kwargs)
        return wrapper
    return inner


@bot.message_handler(func=lambda message: message.text == BACK_TO_MENU_BUTTON.text)
def back_to_menu_handler(message):
    set_menu_state(message.chat.id)
    return bot.send_message(message.chat.id, ph.MENU, reply_markup=MENU_KEYBOARD)


