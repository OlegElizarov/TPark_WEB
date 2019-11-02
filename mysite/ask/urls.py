from django.conf.urls import *
from ask import views

app_name = "ask"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base$', views.base, name='base'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.tag, name='tag'),
    url(r'^settings', views.SView.as_view(), name='settings'),
    url(r'^registration', views.RView.as_view(), name='registration'),

]
