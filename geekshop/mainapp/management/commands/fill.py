import json
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def load_from_json(file_name):
    full_file_name = os.path.join(settings.BASE_DIR, "mainapp", "json", f"{file_name}.json")
    with open(full_file_name, 'r', encoding='utf-8') as f:
        return json.load(f, )


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json("categories")
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)

        products = load_from_json("products")
        Product.objects.all().delete()
        for prod in products:
            _cat = ProductCategory.objects.get(name=prod["category"])
            prod["category"] = _cat
            Product.objects.create(**prod)

        ShopUser.objects.create_superuser("django", "django@local.gb", "geekbrains", age=30)
