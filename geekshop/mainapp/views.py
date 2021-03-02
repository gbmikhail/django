from datetime import datetime
import json

from django.shortcuts import render

# Create your views here.


def main(request):
    content = {
        'title': 'Главная',
        'date': datetime.now()
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    content = {
        'title': 'Продукты',
        'date': datetime.now(),
        'links_menu': links_menu
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
