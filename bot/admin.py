from django.contrib import admin
from .models import *


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "first_name", "last_name")


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "first_name", "username", "date_joined")


@admin.register(CleaningOrder)
class CleaningOrderAdmin(admin.ModelAdmin):
    list_display = ("display_type", "square_metres", "display_trip", "date", "time",
                    "additional_service", "hard_work", "keys_delivery", "very_dirty")

    def display_type(self, obj):
        if obj.type == obj.TYPE_WITH_WINDOWS:
            return "Уборка с окнами"
        else:
            return "Уборка без окон"

    def display_trip(self, obj):
        if obj.trip == obj.DAY_TRIP:
            return Prices.PRICE_DAY_TRIP.value
        elif obj.trip == obj.EVENING_TRIP:
            return Prices.PRICE_EVENING_TRIP.value
        else:
            return Prices.PRICE_NIGHT_TRIP.value
