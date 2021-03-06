from django.conf.urls import *
from ask import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "ask"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^base$', views.base, name='base'),
    url(r'^ask$', views.ask, name='ask'),
    url(r'^question/(?P<question_id>\d+)/$', views.question, name='question'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.tag, name='tag'),
    url(r'^settings', views.settings, name='settings'),
    url(r'^registration', views.RView.as_view(), name='registration'),
    url(r'^login', views.logged_in, name='login'),
    url(r'^logout', views.logged_out, name='logout'),
    url(r'^like', views.like, name='like'),
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
