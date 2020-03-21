from django import forms


class PromocodeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = ((0, "Фиксированная скидка на сумму корзины"), (1, "Процент скидки"))

        self.fields['type'] = forms.ChoiceField(choices=choices)
        self.fields["amount"].max_value = 100
