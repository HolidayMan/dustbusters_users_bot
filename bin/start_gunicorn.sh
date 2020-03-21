#!/bin/bash
source /home/ubuntu/dustbusters_users_bot/venv/bin/activate
#source /home/fsociety/coronabot/venv/bin/postactivate
exec gunicorn -c "/home/ubuntu/dustbusters_users_bot/gunicorn_config.py" dustbusters_users_bot.wsgi
