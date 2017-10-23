from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dummy$', views.dummy),
    url(r'^register$', views.register),
    url(r'^processreg$', views.processreg),
    url(r'^login$', views.login),
    url(r'^processlog$', views.processlog),
    url(r'^items$', views.items),
    url(r'^logout$', views.logout),
    url(r'^(?P<number>\d+)/items$', views.product),
    url(r'^(?P<number>\d+)/addItem$', views.addItem),
    url(r'^checkout$', views.checkout),
]