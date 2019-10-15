from django.conf.urls import *
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'', include('ask.urls', namespace="ask")),
    url(r'^admin/', admin.site.urls ),
    url(r'^accounts/', include('django.contrib.auth.urls')),

]