from django.db import models
import bot.exeptions as exceptions
from .keyboards import DAY_TRIP_BUTTON, EVENING_TRIP_BUTTON,  NIGHT_TRIP_BUTTON
from bot.business_services.prices import CleaningPrices
from .business_services.enums import CleaningTypes, VisitTypes


def cut_phone_number(phone_number):
    return phone_number.replace('+', '')


class Contact(models.Model):
    phone_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    user = models.OneToOneField("TgUser", on_delete=models.CASCADE, related_name="contact")

    @classmethod
    def create_from_contact(cls, contact):
        new_contact = cls()
        contact.phone_number = cut_phone_number(contact.phone_number)
        if not contact.phone_number.strip():
            raise exceptions.NoPhoneNumberError("no phone number")

        new_contact.phone_number = cut_phone_number(contact.phone_number)
        new_contact.first_name = contact.first_name
        new_contact.last_name = contact.last_name
        new_contact.user_id = contact.user_id
        new_contact.user = TgUser.objects.get(tg_id=contact.user_id)
        new_contact.save()
        return new_contact

    def __str__(self):
        return self.first_name


class TgUser(models.Model):
    tg_id = models.IntegerField()
    first_name = models.CharField(max_length=64, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.username:
            return self.username
        else:
            return str(self.id)


class AdditionalService(models.Model):  # TODO: add initial data to fixtures
    name = models.CharField(max_length=256)


class CleaningOrder(models.Model):  # TODO: refactor code
    windows = models.BooleanField(default=False)
    type = models.IntegerField(blank=True, null=True)  # CleaningType
    visit = models.IntegerField(blank=True, null=True)
    place_size = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    additional_services = models.ManyToManyField("AdditionalService", related_name="cleaning_orders")
    user = models.ForeignKey("TgUser", on_delete=models.CASCADE, related_name="cleaning_orders")

    TYPE_WITHOUT_WINDOWS = 0
    TYPE_WITH_WINDOWS = 1

    DAY_TRIP = VisitTypes.DAY_VISIT.value
    EVENING_TRIP = VisitTypes.EVENING_VISIT.value
    NIGHT_TRIP = VisitTypes.NIGHT_VISIT.value

    @staticmethod
    def get_trip_type(trip_name):
        trip_types = {
            DAY_TRIP_BUTTON.text: 0,
            EVENING_TRIP_BUTTON.text: 1,
            NIGHT_TRIP_BUTTON.text: 2
        }
        return trip_types[trip_name]

    def get_per_metre_price(self):
        if self.type == self.TYPE_WITH_WINDOWS:
            return CleaningPrices.PRICE_WITH_WINDOWS.value
        else:
            return CleaningPrices.PRICE_WITHOUT_WINDOWS.value

    def get_trip_price(self):
        if self.visit == self.DAY_TRIP:
            return CleaningPrices.PRICE_DAY_TRIP.value
        elif self.visit == self.EVENING_TRIP:
            return CleaningPrices.PRICE_EVENING_TRIP.value
        elif self.visit == self.NIGHT_TRIP:
            return CleaningPrices.PRICE_NIGHT_TRIP.value
        else:
            return 0

    def get_additional_service_price(self):
        price = 0
        if self.hard_work:
            price += CleaningPrices.PRICE_HARD_WORD.value
        if self.keys_delivery:
            price += CleaningPrices.PRICE_KEYS_DELIVERY.value
        if self.very_dirty:
            price += CleaningPrices.PRICE_VERY_DIRTY.value
        return price

    def calc_price(self):
        price = 0
        price += self.place_size * self.get_per_metre_price()
        price += self.get_trip_price()
        price += self.get_additional_service_price()
        return price
