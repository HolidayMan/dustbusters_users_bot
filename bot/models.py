from django.db import models

import bot.exeptions as exceptions


def cut_phone_number(phone_number):
    return phone_number.replace('+', '')


class Contact(models.Model):
    phone_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    amo_id = models.IntegerField(blank=True, null=True)
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


class AdditionalService(models.Model):
    service_name = models.CharField(max_length=256)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class CleaningOrder(models.Model):
    windows = models.BooleanField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    visit = models.IntegerField(blank=True, null=True)
    place_size = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    additional_services = models.ManyToManyField("AdditionalService", related_name="cleaning_orders")
    user = models.ForeignKey("TgUser", on_delete=models.CASCADE, related_name="cleaning_orders")
    promocode = models.ForeignKey("Promocode", on_delete=models.DO_NOTHING, related_name="cleaning_orders", blank=True, null=True)

    @classmethod
    def new_from_cleaning(cls, cleaning):
        new_order = cls(type=cleaning.cleaning_type,
                        user=cleaning.user)
        if cleaning.visit is not None:
            new_order.visit = cleaning.visit
        if cleaning.visit_time:
            new_order.time = cleaning.visit_time
        if cleaning.visit_date:
            new_order.date = cleaning.visit_date
        if cleaning.windows:
            new_order.windows = cleaning.windows
        if cleaning.place_size:
            new_order.place_size = cleaning.place_size
        return new_order


class Promocode(models.Model):
    promocode = models.CharField(max_length=256)
    type = models.IntegerField()
    amount = models.IntegerField()

    def __str__(self):
        return self.promocode
