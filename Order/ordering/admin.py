from django.contrib import admin

from .models import (OrderItem,
                     Dish,
                     Order)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    empty_value_display = 'Не задано'


class DishInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    inlines = (
        DishInline,
    )

    list_display = (
        'table_number',
        'total_price',
    )
    empty_value_display = 'Не задано'
