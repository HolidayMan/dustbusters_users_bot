from bot.models import Promocode as PromocodeModel
from .enums import PromocodeTypes


class Promocode:
    promocode: str = None
    promo_type: int = None
    amount: int = None
    instance: PromocodeModel = None

    def __init__(self, promocode: str, promo_type: int, amount: int, instance: PromocodeModel = None):
        self.promocode = promocode
        self.promo_type = promo_type
        self.amount = amount
        self.instance = instance

    def _calc_discount_with_percent(self, price):
        return int(price - (price * (self.amount / 100)))

    def _calc_discount_without_percent(self, price):
        return price - self.amount

    def calc_discount(self, price):
        if self.promo_type == PromocodeTypes.PERCENT.value:
            return self._calc_discount_with_percent(price)
        elif self.promo_type == PromocodeTypes.NOT_PERCENT.value:
            return self._calc_discount_without_percent(price)

    @classmethod
    def from_instance(cls, instance: PromocodeModel):
        promocode: str = instance.promocode
        promo_type: int = instance.type
        amount: int = instance.amount

        return cls(promocode, promo_type, amount, instance)

    def to_model(self):
        if self.instance:
            return self.instance
        else:
            raise NotImplementedError  # TODO: here must be creating new promocode
