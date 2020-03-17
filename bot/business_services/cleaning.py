from datetime import date, time
from typing import Union, List

from django.db.models.base import ModelBase

from bot.models import CleaningOrder, TgUser
from .additional_services import CleaningAdditionalServices, AdditionalService
from .enums import CleaningTypes, VisitTypes, CleaningNames, CleaningWindowsTypes, CleaningWindowsNames, VisitNames
from .prices import SoftCleaningPrices, CapitalCleaningPrices, ThoroughCleaningPrices, AbsolutCleaningPrices
from .amo_objects import save_lead_with_contact, Lead

CLEANINGS = {}


def register_cleaning(cleaning_class):
    if cleaning_class.cleaning_type is not None:
        CLEANINGS[cleaning_class.cleaning_type] = cleaning_class


class HelloMeta(type):
    def __new__(mcs, name, bases, _dict):
        new_cls = super().__new__(mcs, name, bases, _dict)
        register_cleaning(new_cls)
        return new_cls


class Cleaning(metaclass=HelloMeta):
    name: str = None
    cleaning_type: int = None
    price_without_windows: int = None
    price_with_windows: int = None
    price_day_visit: int = None
    price_evening_visit: int = None
    price_night_visit: int = None
    windows: bool = None
    visit: int = None
    visit_date: date = None
    visit_time: time = None
    user: TgUser = None
    additional_services: List[AdditionalService] = None
    place_size: int = None
    model: ModelBase = CleaningOrder
    instance: CleaningOrder = None

    def __init__(self, user: Union[TgUser, int], windows: bool, visit: int, place_size: int,
                 additional_services: List[AdditionalService] = None,
                 visit_date: date = None, visit_time: time = None, instance: CleaningOrder = None):
        if isinstance(user, TgUser):
            self.user = user
        else:
            self.user = TgUser.objects.get(tg_id=user)
        self.windows = windows
        self.visit = visit
        self.place_size = place_size
        self.visit_date = visit_date
        self.visit_time = visit_time

        if not additional_services:
            self.additional_services = [service(self) for service in
                                        CleaningAdditionalServices.getobjects()]
        else:
            self.additional_services = additional_services

        self.instance = instance

    @classmethod
    def from_instance(cls, instance: CleaningOrder):
        user: TgUser = instance.user
        windows: bool = instance.windows
        visit: int = instance.visit
        place_size: int = instance.place_size
        visit_date: date = instance.date
        visit_time: time = instance.time

        new_object = cls(user=user, windows=windows, visit=visit, place_size=place_size,
                         visit_date=visit_date, visit_time=visit_time, instance=instance)
        additional_services_names = [service.service_name for service in instance.additional_services.all()]
        additional_services = [
            service(new_object, True) if service.clsname in additional_services_names else service(
                new_object)
            for service in CleaningAdditionalServices.getobjects()]
        if not additional_services:
            additional_services = []
        new_object.additional_services = additional_services
        return new_object

    def calc_price_for_additional_services(self, total):
        price = 0
        for service in self.additional_services:
            if service.clsname == CleaningAdditionalServices.ECO_CLEANING.value.clsname:
                if service.chosen:
                    price += service.get_price_without_selfprice(total + price)
                continue
            if service.chosen:
                price += service.get_price(total + price)
        return price

    def get_cleaning_price(self):
        if not self.place_size:
            return 0
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
        else:
            return 0

    def calc_price(self):
        total = 0
        total += self.get_cleaning_price()
        total += self.get_visit_price()
        total += self.calc_price_for_additional_services(total)
        return total

    def save(self):
        cleaning_db: CleaningDB = CleaningDB(self)
        cleaning_db.save()

    def save_to_amocrm(self):
        amosaver = AmoWorker(self)
        return amosaver.send()


class CleaningDB:

    def __init__(self, cleaning: Cleaning):
        self.cleaning = cleaning
        if not self.cleaning.instance:
            self.instance = CleaningOrder.new_from_cleaning(self.cleaning)
        else:
            self.instance = cleaning.instance

    def save(self):
        self.instance.type = self.cleaning.cleaning_type

        if self.cleaning.visit is not None:
            self.instance.visit = self.cleaning.visit
        if self.cleaning.visit_time:
            self.instance.time = self.cleaning.visit_time
        if self.cleaning.visit_date:
            self.instance.date = self.cleaning.visit_date
        if self.cleaning.windows is not None:
            self.instance.windows = self.cleaning.windows
        if self.cleaning.place_size:
            self.instance.place_size = self.cleaning.place_size
        for service in self.cleaning.additional_services:
            if self.instance.additional_services.filter(
                    service_name=service.clsname).exists() and not service.chosen:
                self.instance.additional_services.remove(service.to_model())
            if service.chosen:
                self.instance.additional_services.add(service.to_model())

        self.instance.save()


class AmoWorker:
    def __init__(self, cleaning):
        self.cleaning = cleaning

    def get_name(self) -> str:
        return f"Заявка с бота №{self.cleaning.instance.id}"

    def get_cleaning_type(self) -> str:
        for windows_type in CleaningWindowsTypes:
            if int(windows_type.value) == self.cleaning.windows:
                return CleaningWindowsNames[windows_type.name].value

    def get_visit(self):
        for visit_type in VisitTypes:
            if int(visit_type.value) == self.cleaning.visit:
                return VisitNames[visit_type.name].value

    def get_visit_datetime(self) -> str:
        return self.cleaning.visit_date.strftime("%Y-%m-%d ") + self.cleaning.visit_time.strftime("%H:%M:00")

    def get_additional_services(self):
        return [service.name for service in self.cleaning.additional_services if service.chosen]

    def send(self) -> Lead:
        if self.get_additional_services():
            new_lead = Lead(
                name=self.get_name(),
                status="Первичный контакт",
                cleaning_type=self.cleaning.name,
                windows=self.get_cleaning_type(),
                place_size=self.cleaning.place_size,
                visit=self.get_visit(),
                visit_date_and_time=self.get_visit_datetime(),
                additional_services=self.get_additional_services(),
                price=str(self.cleaning.calc_price())
            )
        else:
            new_lead = Lead(
                name=self.get_name(),
                status="Первичный контакт",
                cleaning_type=self.cleaning.name,
                windows=self.get_cleaning_type(),
                place_size=self.cleaning.place_size,
                visit=self.get_visit(),
                visit_date_and_time=self.get_visit_datetime(),
                price=str(self.cleaning.calc_price())
            )
        save_lead_with_contact(new_lead, self.cleaning.user.contact.amo_id)
        return new_lead


class SoftCleaning(Cleaning):
    name: str = CleaningNames.SOFT_CLEANING.value
    cleaning_type: int = CleaningTypes.SOFT_CLEANING.value
    price_with_windows: int = SoftCleaningPrices.PRICE_WITH_WINDOWS.value
    price_without_windows: int = SoftCleaningPrices.PRICE_WITHOUT_WINDOWS.value
    price_day_visit: int = SoftCleaningPrices.PRICE_DAY_VISIT.value
    price_evening_visit: int = SoftCleaningPrices.PRICE_EVENING_VISIT.value
    price_night_visit: int = SoftCleaningPrices.PRICE_NIGHT_VISIT.value


class CapitalCleaning(Cleaning):
    name: str = CleaningNames.CAPITAL_CLEANING.value
    cleaning_type: int = CleaningTypes.CAPITAL_CLEANING.value
    price_with_windows: int = CapitalCleaningPrices.PRICE_WITH_WINDOWS.value
    price_without_windows: int = CapitalCleaningPrices.PRICE_WITHOUT_WINDOWS.value
    price_day_visit: int = CapitalCleaningPrices.PRICE_DAY_VISIT.value
    price_evening_visit: int = CapitalCleaningPrices.PRICE_EVENING_VISIT.value
    price_night_visit: int = CapitalCleaningPrices.PRICE_NIGHT_VISIT.value


class ThoroughCleaning(Cleaning):
    name: str = CleaningNames.THOROUGH_CLEANING.value
    cleaning_type: int = CleaningTypes.THOROUGH_CLEANING.value
    price_with_windows: int = ThoroughCleaningPrices.PRICE_WITH_WINDOWS.value
    price_without_windows: int = ThoroughCleaningPrices.PRICE_WITHOUT_WINDOWS.value
    price_day_visit: int = ThoroughCleaningPrices.PRICE_DAY_VISIT.value
    price_evening_visit: int = ThoroughCleaningPrices.PRICE_EVENING_VISIT.value
    price_night_visit: int = ThoroughCleaningPrices.PRICE_NIGHT_VISIT.value


class AbsolutCleaning(Cleaning):
    name: str = CleaningNames.ABSOLUT_CLEANING.value
    cleaning_type: int = CleaningTypes.ABSOLUT_CLEANING.value
    price_with_windows: int = AbsolutCleaningPrices.PRICE_WITH_WINDOWS.value
    price_without_windows: int = AbsolutCleaningPrices.PRICE_WITHOUT_WINDOWS.value
    price_day_visit: int = AbsolutCleaningPrices.PRICE_DAY_VISIT.value
    price_evening_visit: int = AbsolutCleaningPrices.PRICE_EVENING_VISIT.value
    price_night_visit: int = AbsolutCleaningPrices.PRICE_NIGHT_VISIT.value
