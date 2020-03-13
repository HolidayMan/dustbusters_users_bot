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
    list_display = ("display_type", "user", "display_windows", "place_size", "display_trip", "date", "time",
                    "display_additional_service")  # "additional_service", "hard_work", "keys_delivery", "very_dirty",

    def display_additional_service(self, obj: CleaningOrder):
        return " ,".join(obj.additional_services.all()) if obj.additional_services.all() else "Не выбрано"

    def display_type(self, obj: CleaningOrder):
        if obj.visit == obj.TYPE_WITH_WINDOWS:
            return "Уборка с окнами"
        elif obj.visit == obj.TYPE_WITHOUT_WINDOWS:
            return "Уборка без окон"
        else:
            return "Не выбрано"

    def display_windows(self, obj: CleaningOrder):
        if obj.windows:
            return "Уборка с окнами"
        elif isinstance(obj.windows, bool) and not obj.windows:
            return "Уборка без окон"
        else:
            return "Не выбрано"

    def display_trip(self, obj: CleaningOrder):
        if obj.visit == obj.DAY_TRIP:
            return "День"
        elif obj.visit == obj.EVENING_TRIP:
            return "Вечер"
        elif obj.visit == obj.NIGHT_TRIP:
            return "Ночь"
        else:
            return "Не выбрано"

    display_type.short_description = "Cleaning type"
    display_windows.short_description = "Cleaning type"
    display_trip.short_description = "Trip time"
    display_additional_service.short_description = "Additional services"
