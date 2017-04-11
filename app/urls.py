from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/add/$', views.cad_user, name='cad_user'),
    url(r'^item/add/$', views.cad_item, name='cad_item'),
]
