from django.conf.urls import url
from . import views

app_name = 'communities_app'

urlpatterns = [
    url(r'^communities/?', views.CommunityViewSet.as_view({'get': 'list'})),
    url(r'^community/(?P<url_name>[a-zA-Z0-9\._]{1,20})/?$', views.CommunityView.as_view()),
    url(r'^graph/community/(?P<url_name>[a-zA-Z0-9\._]{1,20})/(?P<graph_name>[a-zA-Z0-9\._]{1,20})/?$',
        views.get_community_graph),
]
