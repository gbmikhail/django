import datetime
import os
from collections import OrderedDict
from urllib.parse import urlunparse, urlencode

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user: ShopUser, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_max&access_token={response['access_token']}&v=5.92"
    # api_url = urlunparse((
    #     'https',
    #     'api.vk.com',
    #     '/method/users.get',
    #     None,
    #     urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                           access_token=response['access_token'],
    #                           v='5.92')),
    #     None
    # ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        print("VK Error", resp.status_code)
        return

    data = resp.json()['response'][0]
    print(data)

    if data['sex'] == 1:
        user.shopuserprofile.gender = ShopUserProfile.FEMALE
    elif data['sex'] == 2:
        user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = datetime.datetime.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    if data['photo_max']:
        # users_avatar/product-3.jpg
        avatar = user.avatar
        if True: #not avatar:
            photo = requests.get(data['photo_max'])
            if photo.status_code == 200:
                fl_name = f'{user.id}.jpg'
                avatar = os.path.join('users_avatar', fl_name)

                user.avatar = avatar
                avatar = os.path.join(settings.MEDIA_ROOT, avatar)
                with open(avatar, 'wb') as file:
                    file.write(photo.content)

    if data['id']:
        user.shopuserprofile.vk_id = data['id']

    user.save()
