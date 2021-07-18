from django.conf.urls import url
from products import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^api/category$',views.CategoryApi),
    url(r'^api/category/([0-9]+)$',views.CategoryApi)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)