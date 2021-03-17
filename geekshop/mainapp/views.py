from datetime import datetime
import json
import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    basket = []
    if user.is_authenticated:
        basket = Basket.objects.filter(user=user)
    return basket


def get_hot_product():
    product_list = Product.objects.all()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_product = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_product


def main(request):
    products = Product.objects.all()[:4]

    content = {
        'title': 'Главная',
        'products': products,
        'date': datetime.now(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    # basket = 0
    # if request.user.is_authenticated:
    #     basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))

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
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products_list.html', content)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    content = {
        'title': 'Продукт',
        'date': datetime.now(),
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)


def contacts(request):
    from geekshop.settings import BASE_DIR
    with open(BASE_DIR / "contacts.json", 'r', encoding='utf-8') as json_data_file:
        contacts_list = json.load(json_data_file)

    content = {
        'title': 'Контакты',
        'date': datetime.now(),
        'contacts': contacts_list,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)
