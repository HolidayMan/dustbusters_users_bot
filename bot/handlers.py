from .bot import bot
import bot.phrases as ph
from .utils import set_menu_state
from .keyboards import BACK_TO_MENU_BUTTON, MENU_KEYBOARD
from .models import TgUser

@bot.message_handler(func=lambda message: message.text == BACK_TO_MENU_BUTTON.text)
def back_to_menu_handler(message):
    set_menu_state(message.chat.id)
    return bot.send_message(message.chat.id, ph.MENU, reply_markup=MENU_KEYBOARD)


def handle_back_to_menu(func, delete=False, model=None):
    def wrapper(message, *args, **kwargs):
        if message.text == BACK_TO_MENU_BUTTON.text:
            if delete:
                user = TgUser.objects.get(tg_id=message.chat.id)
                object = model.objects.filter(user=user).order_by("-id")[0]
                object.delete()
            return back_to_menu_handler(message)
        else:
            return func(message, *args, **kwargs)
    return wrapper