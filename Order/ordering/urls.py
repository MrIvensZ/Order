from django.urls import path

from .views import (create_order,
                    order_detail,
                    delete_order,
                    order_change_status)

app_name = 'ordering'

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('<int:order_pk>/detail', order_detail, name='order_detail'),
    path('<int:order_pk>/delete', delete_order, name='delete_order'),
    path('<int:order_pk>/status', order_change_status, name='order_status'),
]
