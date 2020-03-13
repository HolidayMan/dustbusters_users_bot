from datetime import date, time

from django.db.models.base import ModelBase

from bot.models import CleaningOrder
from .additional_services import CleaningAdditionalServices
from .enums import VisitTypes


class Cleaning:  # TODO: add db saver, create Cleanings
    name: str = None
    cleaning_type: int = None
    windows: bool = None
    visit: int = None
    visit_date: date = None
    visit_time: time = None
    price_with_windows: int = None
    price_without_windows: int = None
    price_day_visit: int = None
    price_evening_visit: int = None
    price_night_visit: int = None
    additional_services: list = None
    place_size: int = None
    model: ModelBase = CleaningOrder

    def __init__(self, cleaning_type: int, windows: bool, visit: int, place_size: int, additional_services: list = None,
                 visit_date: date = None, visit_time: time = None, instance: CleaningOrder = None):
        self.cleaning_type = cleaning_type
        self.windows = windows
        self.visit = visit
        self.place_size = place_size
        self.visit_date = visit_date
        self.visit_time = visit_time

        if not additional_services:
            self.additional_services = [service() for service in CleaningAdditionalServices.getobjects()]
        else:
            self.additional_services = additional_services

        self.instance = instance

    @classmethod
    def from_instance(cls, instance: CleaningOrder):
        cleaning_type = instance.type
        windows: bool = instance.windows
        visit: int = instance.visit
        place_size: int = instance.place_size
        visit_date: date = instance.date
        visit_time: time = instance.time
        additional_services_names = [service.name for service in instance.additional_services]
        additional_services = [service(True) if service.clsname in additional_services_names else service()
                               for service in CleaningAdditionalServices.getobjects()]
        return cls(cleaning_type=cleaning_type, windows=windows, visit=visit, place_size=place_size, additional_services=additional_services,
                   visit_date=visit_date, visit_time=visit_time, instance=instance)

    def calc_price_for_additional_services(self):
        return sum(service.price[self.cleaning_type] for service in self.additional_services if service.chosen)

    def get_cleaning_price(self):
        if self.windows:
            return self.place_size * self.price_with_windows
        else:
            return self.place_size * self.price_without_windows

    def get_visit_price(self):
        if self.visit == VisitTypes.DAY_VISIT.value:
            return self.price_day_visit
        elif self.visit == VisitTypes.EVENING_VISIT.value:
            return self.price_evening_visit
        elif self.visit == VisitTypes.NIGHT_VISIT.value:
            return self.price_night_visit

    def calc_price(self):
        total = 0
        total += self.get_cleaning_price()
        total += self.get_visit_price()
        total += self.calc_price_for_additional_services()
        return total
