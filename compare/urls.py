from django.conf.urls import url
from compare import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^search$',views.SearchApi),
    url(r'^search/([0-9]+)$',views.SearchApi)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)