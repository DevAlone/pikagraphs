from django.conf.urls import url
from . import views
app_name = 'core'

urlpatterns = [
    url(r'^users/?$', views.UserViewSet.as_view({'get': 'list'})),
    url(r'^user/(?P<username>[a-zA-Z0-9\._]{1,20})/?$', views.UserView.as_view()),
    url(r'^graph/user/(?P<username>[a-zA-Z0-9\._]{1,20})/(?P<graph_name>[a-zA-Z0-9\._]{1,20})/?$',
        views.get_user_graph),

    url(r'^pikabu_users/?$', views.PikabuUserViewSet.as_view({'get': 'list'})),

    url(r'^push_users_info/(?P<session>[a-zA-Z0-9_\-]{1,64})/$', views.push_users_info),
]
