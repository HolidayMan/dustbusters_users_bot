from .bot import bot
import bot.phrases as ph
from bot.business_services.utils import create_user, user_exists, contact_exists, set_menu_state
from .models import Contact
from .keyboards import AUTHORIZE_KEYBOARD, MENU_KEYBOARD
from bot.business_services.amo_objects import Contact as Amocontact

@bot.message_handler(commands=['start', 'help'])
def cmd_start(message):
    if not user_exists(message):
        create_user(message)

    if not contact_exists(message):  # then authorizing user
        bot.register_next_step_handler(message, authorize_user)
        return bot.send_message(message.chat.id, ph.PLEASE_AUTHORIZE, parse_mode="HTML", reply_markup=AUTHORIZE_KEYBOARD)

    set_menu_state(message.chat.id)
    return bot.send_message(message.chat.id, ph.HELP_MESSAGE, parse_mode="HTML", reply_markup=MENU_KEYBOARD)


def authorize_user(message):
    if message.contact:
        contact = message.contact
        if contact.phone_number:
            new_contact = Contact.create_from_contact(contact)
            set_menu_state(message.chat.id)

            name = ""
            if new_contact.user.username:
                name += new_contact.user.username
            elif new_contact.first_name:
                name += new_contact.first_name
            elif new_contact.last_name:
                name += new_contact.last_name

            amocontact = Amocontact(name=name, phone=new_contact.phone_number, tags="telegram")
            amocontact.save()
            new_contact.amo_id = amocontact.id
            new_contact.save()
            return bot.send_message(message.chat.id, ph.YOU_WERE_AUTHORIZED_AS % new_contact.phone_number, parse_mode="HTML", reply_markup=MENU_KEYBOARD)
        else:
            bot.register_next_step_handler(message, authorize_user)
            return bot.send_message(message.chat.id, ph.INVALID_CONTACT, parse_mode="HTML", reply_markup=AUTHORIZE_KEYBOARD)
    else:
        bot.register_next_step_handler(message, authorize_user)
        return bot.send_message(message.chat.id, ph.INVALID_CONTACT, parse_mode="HTML", reply_markup=AUTHORIZE_KEYBOARD)
