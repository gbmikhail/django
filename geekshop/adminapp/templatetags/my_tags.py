from django import template
from django.conf import settings


register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(path_to_avatar):
    if not path_to_avatar:
        path_to_avatar = 'users_avatar/default.png'
    return f'{settings.MEDIA_URL}{path_to_avatar}'


# @register.filter(name='media_for_products')
def media_for_products(path_to_avatar):
    if not path_to_avatar:
        path_to_avatar = 'products_images/default.png'
    return f'{settings.MEDIA_URL}{path_to_avatar}'


register.filter('media_for_products', media_for_products)
