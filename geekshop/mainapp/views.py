from datetime import datetime
import json

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
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
    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

    links_menu = ProductCategory.objects.all()
    if pk is not None:
        # category_item = ProductCategory.objects.filter(pk=pk).first()
        category_item = get_object_or_404(ProductCategory, pk=pk)
        products_list = Product.objects.filter(category=category_item)
    else:
        products_list = Product.objects.all().order_by('price')
        category_item = {'name': 'Все', 'pk': 0}

    content = {
        'title': 'Продукты',
        'date': datetime.now(),
        'links_menu': links_menu,
        'category': category_item,
        'products': products_list,
        'basket': basket
    }
    return render(request, 'mainapp/products_list.html', content)

    # same_products = Product.objects.all()[:4]
    # content = {
    #     'title': 'Продукты',
    #     'date': datetime.now(),
    #     'links_menu': links_menu,
    #     'same_products': same_products,
    #     'basket': basket
    # }
    # return render(request, 'mainapp/products.html', content)


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
