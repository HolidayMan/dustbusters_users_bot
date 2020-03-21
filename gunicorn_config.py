command = '/home/ubuntu/dustbusters_users_bot/venv/bin/gunicorn'
pythonpath = '/home/ubuntu/dustbusters_users_bot'
bind = '127.0.0.1:8001'
workers = 1
user = 'ubuntu'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=dustbusters_users_bot.settings'
