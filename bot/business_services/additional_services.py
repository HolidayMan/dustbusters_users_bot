from enum import Enum

from bot.models import AdditionalService as AdditionalServiceModel
from .enums import CleaningTypes


class AdditionalService:
    prices: dict = None
    name: str = None
    chosen: bool = False

    def __init__(self, service_type: int, chosen: bool = False):
        self.service_type = service_type
        self.chosen = chosen

    def get_price(self, service_type: int):
        return self.prices[service_type]

    def build_name(self):
        return self.name % self.get_price(self.service_type)

    @staticmethod
    def from_instance(instance):
        name = instance.name
        for service in CleaningAdditionalServices:
            if service.value.name == name:
                return service()
        raise ValueError("no such additional service exists")

    def to_model(self):
        return AdditionalServiceModel.objects.get(name=self.clsname)


class AdditionalServiceClass(type):

    def __new__(mcs, clsname, *args, bases=(AdditionalService,), _dict={}, **kwargs):
        new_additional_service = super().__new__(mcs, clsname, bases, _dict)
        return new_additional_service

    def __init__(cls, clsname, name, prices):
        cls.clsname = clsname
        cls.name = name
        cls.prices = prices


class CleaningAdditionalServices(Enum):
    COMPLEX_CHANDELIER = AdditionalServiceClass(
        "CLEANING_COMPLEX_CHANDELIER",
        "Сложная разборная \\ хрустальная люстра: от %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 1000,
            CleaningTypes.CAPITAL_CLEANING.value: 1000,
            CleaningTypes.THOROUGH_CLEANING.value: 1000,
            CleaningTypes.ABSOLUT_CLEANING.value: 1000,
        })

    KEYS_DELIVERY = AdditionalServiceClass(
        "CLEANING_KEYS_DELIVERY",
        "Доставка ключей: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 500,
            CleaningTypes.CAPITAL_CLEANING.value: 500,
            CleaningTypes.THOROUGH_CLEANING.value: 500,
            CleaningTypes.ABSOLUT_CLEANING.value: 500,
        })

    IRONING = AdditionalServiceClass(
        "CLEANING_IRONING",
        "Глажка белья: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 500,
            CleaningTypes.CAPITAL_CLEANING.value: 500,
            CleaningTypes.THOROUGH_CLEANING.value: 500,
            CleaningTypes.ABSOLUT_CLEANING.value: 500,
        })

    ADDITIONAL_BATHROOM = AdditionalServiceClass(
        "CLEANING_ADDITIONAL_BATHROOM",
        "Дополнительный с/у: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 500,
            CleaningTypes.CAPITAL_CLEANING.value: 500,
            CleaningTypes.THOROUGH_CLEANING.value: 500,
            CleaningTypes.ABSOLUT_CLEANING.value: 500,
        })

    BALCONY_CLEANING = AdditionalServiceClass(
        "CLEANING_BALCONY_CLEANING",
        "Уборка на балконе: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 500,
            CleaningTypes.CAPITAL_CLEANING.value: 500,
            CleaningTypes.THOROUGH_CLEANING.value: 500,
            CleaningTypes.ABSOLUT_CLEANING.value: 500,
        })

    VERY_DIRTY = AdditionalServiceClass(
        "CLEANING_VERY_DIRTY",
        "Высокая степень загрязнения от: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 1000,
            CleaningTypes.CAPITAL_CLEANING.value: 1000,
            CleaningTypes.THOROUGH_CLEANING.value: 1000,
            CleaningTypes.ABSOLUT_CLEANING.value: 1000,
        })

    EQUIPMENT_DELIVERY_MOSCOW = AdditionalServiceClass(
        "CLEANING_EQUIPMENT_DELIVERY_MOSCOW",
        "Доставка оборудования по Москве: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 1000,
            CleaningTypes.CAPITAL_CLEANING.value: 1000,
            CleaningTypes.THOROUGH_CLEANING.value: 1000,
            CleaningTypes.ABSOLUT_CLEANING.value: 1000,
        })

    EQUIPMENT_DELIVERY_MKAD = AdditionalServiceClass(
        "CLEANING_EQUIPMENT_DELIVERY_MKAD",
        "Доставка оборудования за МКАД от: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 1500,
            CleaningTypes.CAPITAL_CLEANING.value: 1500,
            CleaningTypes.THOROUGH_CLEANING.value: 1500,
            CleaningTypes.ABSOLUT_CLEANING.value: 1500,
        })

    ECO_CLEANING = AdditionalServiceClass(
        "CLEANING_ECO_CLEANING",
        "Эко-уборка от: %s",
        {
            CleaningTypes.SOFT_CLEANING.value: 1080,
            CleaningTypes.CAPITAL_CLEANING.value: 1800,
            CleaningTypes.THOROUGH_CLEANING.value: 1440,
            CleaningTypes.ABSOLUT_CLEANING.value: 1800,
        })

    @classmethod
    def getobjects(cls):
        return [attr.value for attr in cls]
