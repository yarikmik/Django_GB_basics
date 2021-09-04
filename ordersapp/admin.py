from django.contrib import admin

from ordersapp.models import Order


@admin.register(Order)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated", "status")  # добавление колонок в админку
    list_filter = ("created", "user")
