from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0)
    add_datetime = models.DateTimeField(auto_now=True, verbose_name='Время')

    # # Связка уникальных полей
    # class Meta:
    #     unique_together = ('user', 'product')
