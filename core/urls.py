from django.conf.urls import url
from . import views

app_name = 'core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<username>[a-z0-9\._]{1,20})/$', views.user, name='user'),
]
