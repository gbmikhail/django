# Generated by Django 3.1.7 on 2021-04-08 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_shopuserprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='vk_id',
            field=models.TextField(blank=True, max_length=128, null=True, verbose_name='id ВКонтакте'),
        ),
    ]
