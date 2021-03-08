from django.db import models


class ProductCategory(models.Model):
    # id = models.BigAutoField(primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=64, unique=True, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name="Имя")
    image = models.ImageField(upload_to="products_images", blank=True)
    short_desc = models.CharField(max_length=64, verbose_name="Краткое описание", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество на складе", default=0)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
