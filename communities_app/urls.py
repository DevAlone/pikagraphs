from django.conf.urls import url
from . import views

app_name = 'communities_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^community/(?P<urlName>[a-zA-Z0-9\._]{1,20})/$',
        views.community, name='community'),
    url(r'^secret_page_for_lactarius/$', views.secret_page_for_lactarius,
        name='secret_page_for_lactarius'),
]
