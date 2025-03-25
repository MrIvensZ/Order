from django.contrib import admin
from django.urls import path, include

from ordering.views import index, total_price, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ordering/', include('ordering.urls')),
    path('', index, name='index'),
    path('total_price', total_price, name='total_price'),
    path('search', search, name='search')
]
