import os
from dustbusters_users_bot.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TOKEN = "<your token>"

SECRET_KEY = '<your SECRET_KEY>' # django SECRET_KEY

DOMAIN = 'my_domain'

STATES_FILE = os.path.join(BASE_DIR, "states.vdb")
LOG_FILE = os.path.join(BASE_DIR, "bot.log")

AMO_API_KEY = "api_key"
AMO_LOGIN = "amo_login"
AMO_SUBDOMAIN = "amo_subdomain"
