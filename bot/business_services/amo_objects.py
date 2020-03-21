from amocrm import BaseContact, amo_settings, fields, BaseLead
from dustbusters_users_bot.settings import AMO_API_KEY, AMO_LOGIN, AMO_SUBDOMAIN

amo_settings.set(AMO_LOGIN, AMO_API_KEY, AMO_SUBDOMAIN)


def save_lead_with_contact(self: BaseLead, contact_id: BaseContact, update_if_exists=False):
    self._save_fk()
    self._pre_save()
    contacts = {"contacts_id": [contact_id]}
    self._data.update(contacts)
    data = self._data
    if self.id is not None:
        method = self.objects.update
        if not self._changed_fields:
            return
        data = dict([(key, value) for key, value in data.items() if key in self._changed_fields or key in self._required])
    elif update_if_exists:
        method = self.objects.create_or_update
    else:
        method = self.objects.create
    result = method(**data)
    if result:
        self._data['id'] = result
    self._changed_fields = []
    self._fields_data = {}


class Contact(BaseContact):
    phone = fields.EnumCustomField('Телефон', enum='WORK')


class Lead(BaseLead):
    cleaning_type = fields.CustomField(u'Название уборки')
    windows = fields.CustomField(u'Тип уборки')
    place_size = fields.CustomField(u'Кол-во м²')
    visit = fields.CustomField(u'Временной промежуток')
    visit_date_and_time = fields.CustomField(u'Дата и время')
    additional_services = fields.CustomField(u'Доп. услуги')
