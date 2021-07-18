from django.contrib import admin
from django.urls import path

from django.conf.urls import url,include

from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('compare.urls')),
    url(r'^', include('products.urls')),
    url(r'^', include('categories.urls'))
]