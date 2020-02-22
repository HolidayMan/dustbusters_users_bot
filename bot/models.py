from django.db import models
import bot.exeptions as exceptions


def cut_phone_number(phone_number):
    return phone_number.replace('+', '')


class Contact(models.Model):
    phone_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    user = models.OneToOneField("TgUser", on_delete=models.CASCADE)

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
