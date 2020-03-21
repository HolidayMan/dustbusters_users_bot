from django.contrib import admin

from bot.business_services.enums import CleaningNames, CleaningTypes, VisitTypes
from .business_services.utils import get_cleaning_class_from_type
from .models import *
from .forms import PromocodeAdminForm

admin.site.site_header = "Dustbusters User Bot"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "first_name", "last_name", "amo_id")
    search_fields = ('phone_number', "first_name", "last_name")


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_id", "first_name", "username", "date_joined")
    search_fields = ('username', "first_name")


@admin.register(CleaningOrder)
class CleaningOrderAdmin(admin.ModelAdmin):
    list_display = ("display_type", "user", "display_windows", "place_size", "display_trip", "date", "time",
                    "display_additional_service", "promocode")

    def display_additional_service(self, obj: CleaningOrder):
        return ", ".join(service.name for service in
                         obj.additional_services.all()) if obj.additional_services.all() else "Не выбрано"

    def display_type(self, obj: CleaningOrder):
        if obj.type == CleaningTypes.SOFT_CLEANING.value:
            return CleaningNames.SOFT_CLEANING.value
        elif obj.type == CleaningTypes.CAPITAL_CLEANING.value:
            return CleaningNames.CAPITAL_CLEANING.value
        elif obj.type == CleaningTypes.THOROUGH_CLEANING.value:
            return CleaningNames.THOROUGH_CLEANING.value
        elif obj.type == CleaningTypes.ABSOLUT_CLEANING.value:
            return CleaningNames.ABSOLUT_CLEANING.value
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
        if obj.visit == VisitTypes.DAY_VISIT.value:
            return "День"
        elif obj.visit == VisitTypes.EVENING_VISIT.value:
            return "Вечер"
        elif obj.visit == VisitTypes.NIGHT_VISIT.value:
            return "Ночь"
        else:
            return "Не выбрано"

    # def display_price(self, obj: CleaningOrder):
    #     cleaning = get_cleaning_class_from_type(obj.type).from_instance(obj)
    #     return f"{cleaning.calc_price()} ₽"

    display_type.short_description = "Cleaning type"
    display_windows.short_description = "Windows"
    display_trip.short_description = "Trip time"
    display_additional_service.short_description = "Additional services"
    # display_price.short_description = "Total price"


@admin.register(AdditionalService)
class AdditionalSeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class PromocodeTypeFilter(admin.SimpleListFilter):
    title = 'promocode type'

    parameter_name = 'promocode_type'

    related_filter_parameter = 'promocode__type'

    def lookups(self, request, model_admin):
        return (0, "Фиксированная скидка на сумму корзины"), (1, "Процент скидки")

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type=self.value())
        return queryset


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("promocode", "display_type", "amount")
    form = PromocodeAdminForm

    search_fields = ('promocode',)
    list_filter = (PromocodeTypeFilter, "amount")

    def display_type(self, obj):
        if obj.type == 0:
            return "Фиксированная скидка на сумму корзины"
        else:
            return "Процент скидки"

    def get_urls(self):
        urls = super().get_urls()
        return urls

    display_type.short_description = "Type"
