# Generated by Django 3.2.5 on 2021-07-28 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='колличество'),
        ),
    ]