from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'title': 'Корзина',
        'basket_items': basket_items
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):
    # Исправляем зацикливание
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))

    product_item = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()

    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)

    basket_item.quantity = F('quantity') + 1
    if basket_item.quantity == 1:
        basket_item.save()
    else:
        basket_item.save(update_fields=['quantity', 'product'])

    update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
    print(f'query basket_add: {update_queries}')

    # Возвращаем посетителя туда, откуда он пришел
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()

    # Возвращаем посетителя туда, откуда он пришел
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})
