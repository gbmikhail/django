from datetime import datetime
import json

from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def main(request):
    products = Product.objects.all()[:4]

    content = {
        'title': 'Главная',
        'products': products,
        'date': datetime.now()
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    same_products = Product.objects.all()[:4]
    links_menu = ProductCategory.objects.all()
    content = {
        'title': 'Продукты',
        'date': datetime.now(),
        'links_menu': links_menu,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', content)


def contacts(request):
    from geekshop.settings import BASE_DIR
    with open(BASE_DIR / "contacts.json", 'r', encoding='utf-8') as json_data_file:
        contacts_list = json.load(json_data_file)

    content = {
        'title': 'Контакты',
        'date': datetime.now(),
        'contacts': contacts_list
    }
    return render(request, 'mainapp/contact.html', content)
