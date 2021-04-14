from django.conf import settings
from django.db import models

from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(auto_now=True, verbose_name='Время добавления')

    # # Связка уникальных полей
    # class Meta:
    #     unique_together = ('user', 'product')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()

    @classmethod
    def get_product_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dict = {}
        [basket_items_dict.update({item.product: item.quantity}) for item in basket_items]

    @staticmethod
    def get_items(pk):
        return Basket.objects.get(pk=pk)
