# Generated by Django 3.2.5 on 2021-07-29 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0003_alter_basket_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='total_price',
        ),
    ]