from django.contrib import admin
from .models import *


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "first_name", "last_name")


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "first_name", "username", "date_joined")