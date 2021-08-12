from django.contrib import admin
from django.urls import path

from django.conf.urls import url,include

from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/v1/compare/', include('compare.urls')),
    url(r'api/v1/products/', include('products.urls')),
    url(r'api/v1/categories/', include('categories.urls'))
]