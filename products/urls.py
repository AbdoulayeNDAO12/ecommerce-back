from django.conf.urls import url
from products import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^api/product$',views.ProductApi),
    url(r'^api/product/([0-9]+)$',views.ProductApi)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)