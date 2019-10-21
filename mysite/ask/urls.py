from django.conf.urls import *
from ask import views

app_name = "ask"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base$', views.BaseView.as_view(), name='base'),
    url(r'^ask', views.AView.as_view(), name='ask'),
    url(r'^question/(?P<pk>\d+)/$', views.QView.as_view(), name='question'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.tag, name='tag'),
    url(r'^settings', views.SView.as_view(), name='settings'),
    url(r'^registration', views.RView.as_view(), name='registration'),

]
