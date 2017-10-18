from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^user_info/(?P<username>[a-zA-Z0-9\._]{1,20})/$', views.user_info,
        name='user_info'),
    # url(r'^user_graph/(?P<username>[a-zA-Z0-9\._]{1,20})/(?P<type>[a-z]{1, 20})/$', views.user_graph,
    #    name='user_graph'),
    url(r'^user_graph/(?P<username>[a-zA-Z0-9\._]{1,20})/(?P<type>[a-zA-Z0-9\._]{1,20})/$', views.user_graph,
        name='user_graph'),
    url(r'^user_graphs/(?P<username>[a-zA-Z0-9\._]{1,20})/$', views.user_graphs,
        name='user_graphs')
]
