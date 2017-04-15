from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^user/auth/$', views.auth_user, name='auth_user'),
    url(r'^user/logout/$', views.logout, name='logout'),
    url(r'^user/add/$', views.cad_user, name='cad_user'),
    url(r'^item/add/$', views.cad_item, name='cad_item'),
    url(r'^gasto/add/$', views.cad_gasto, name='cad_gasto'),
    url(r'^itens/list/$', views.list_itens, name='list_itens'),
    url(r'^item/delete/(?P<item>\d+)/$', views.delete_item, name='delete_item'),
]
