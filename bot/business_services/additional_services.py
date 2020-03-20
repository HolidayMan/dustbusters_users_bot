from enum import Enum

from bot.models import AdditionalService as AdditionalServiceModel
from .enums import CleaningTypes


class Price:
    price: int = None

    def __init__(self, price):
        self.price = price

    def get_price(self, *args, **kwargs):
        return self.price

    def __str__(self):
        return str(self.price)


class Percent(Price):
    def __init__(self, percent):
        self.percent = percent

    def get_price(self, service):
        return round(service.calc_price() * (self.percent / 100))


class AdditionalService:
    clsname: str = None
    prices: dict = None
    name: str = None
    price_string: str = None
    chosen: bool = False

    def __init__(self, service, chosen: bool = False):
        self.service = service
        self.service_type = service.cleaning_type
        self.chosen = chosen

    def get_price(self, *args):
        return self.prices[self.service.cleaning_type].get_price(self.service)

    def build_name(self):
        return self.price_string % self.get_price()

    def to_model(self):
        return AdditionalServiceModel.objects.get(service_name=self.clsname)


class AdditionalServiceClass(type):

    def __new__(mcs, clsname, *args, bases=(AdditionalService,), _dict={}, **kwargs):
        new_additional_service = super().__new__(mcs, clsname, bases, _dict)
        return new_additional_service

    def __init__(cls, clsname: str, name: str, price_string: str, prices: dict):
        cls.clsname = clsname
        cls.name = name
        cls.price_string = price_string
        cls.prices = prices


class EcoCleaning(AdditionalService):
    clsname = "CLEANING_ECO_CLEANING"
    name = "Эко-уборка"
    price_string = "Эко-уборка: %s"
    prices = {
            CleaningTypes.SOFT_CLEANING.value: Percent(30),
            CleaningTypes.CAPITAL_CLEANING.value: Percent(30),
            CleaningTypes.THOROUGH_CLEANING.value: Percent(30),
            CleaningTypes.ABSOLUT_CLEANING.value: Percent(30),
        }

    def __init__(self, service, chosen: bool = False):
        super().__init__(service, chosen)

    def get_price_without_selfprice(self, current_price):
        percent = self.prices[self.service.cleaning_type].percent

        return round(current_price * (percent / 100))

    def get_price(self):
        percent = self.prices[self.service.cleaning_type].percent

        if self.chosen:
            return self.service.calc_price() - round(self.service.calc_price() / ((100 + percent) / 100))
        else:
            return round(self.service.calc_price() * (percent / 100))

    def build_name(self):
        return self.price_string % self.get_price()


class CleaningAdditionalServices(Enum):
    COMPLEX_CHANDELIER = AdditionalServiceClass(
        "CLEANING_COMPLEX_CHANDELIER",
        "Сложная разборная \\ хрустальная люстра",
        "Сложная разборная \\ хрустальная люстра: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(1000),
            CleaningTypes.CAPITAL_CLEANING.value: Price(1000),
            CleaningTypes.THOROUGH_CLEANING.value: Price(1000),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(1000),
        })

    KEYS_DELIVERY = AdditionalServiceClass(
        "CLEANING_KEYS_DELIVERY",
        "Доставить ключи",
        "Доставить ключи: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(500),
        })

    KEYS_TAKING = AdditionalServiceClass(
        "KEYS_TAKING",
        "Забрать ключи",
        "Забрать ключи: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(500),
        })

    IRONING = AdditionalServiceClass(
        "CLEANING_IRONING",
        "Глажка белья",
        "Глажка белья: %s в час",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(500),
        })

    ADDITIONAL_BATHROOM = AdditionalServiceClass(
        "CLEANING_ADDITIONAL_BATHROOM",
        "Дополнительный с/у",
        "Дополнительный с/у: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(500),
        })

    BALCONY_CLEANING = AdditionalServiceClass(
        "CLEANING_BALCONY_CLEANING",
        "Уборка на балконе",
        "Уборка на балконе: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(1500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(1500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(1500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(1500),
        })

    VERY_DIRTY = AdditionalServiceClass(
        "CLEANING_VERY_DIRTY",
        "Высокая степень загрязнения",
        "Высокая степень загрязнения: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(1000),
            CleaningTypes.CAPITAL_CLEANING.value: Price(1000),
            CleaningTypes.THOROUGH_CLEANING.value: Price(1000),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(1000),
        })

    EQUIPMENT_DELIVERY_MOSCOW = AdditionalServiceClass(
        "CLEANING_EQUIPMENT_DELIVERY_MOSCOW",
        "Доставка оборудования по Москве",
        "Доставка оборудования по Москве: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(1000),
            CleaningTypes.CAPITAL_CLEANING.value: Price(1000),
            CleaningTypes.THOROUGH_CLEANING.value: Price(1000),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(1000),
        })

    EQUIPMENT_DELIVERY_MKAD = AdditionalServiceClass(
        "CLEANING_EQUIPMENT_DELIVERY_MKAD",
        "Доставка оборудования за МКАД",
        "Доставка оборудования за МКАД: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: Price(1500),
            CleaningTypes.CAPITAL_CLEANING.value: Price(1500),
            CleaningTypes.THOROUGH_CLEANING.value: Price(1500),
            CleaningTypes.ABSOLUT_CLEANING.value: Price(1500),
        })

    ECO_CLEANING = EcoCleaning

    @classmethod
    def getobjects(cls):
        return [attr.value for attr in cls]
