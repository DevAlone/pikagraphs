from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [
    url(r'^users/?$', views.UserViewSet.as_view({'get': 'list'})),
    url(r'^user/(?P<username>[a-zA-Z0-9\._]{1,20})/?$', views.UserView.as_view()),
    url(r'^graph/user/(?P<username>[a-zA-Z0-9\._]{1,20})/(?P<graph_name>[a-zA-Z0-9\._]{1,20})/?$',
        views.get_user_graph),

    url(r'^communities/?', views.CommunityViewSet.as_view({'get': 'list'})),
    url(r'^community/(?P<url_name>[a-zA-Z0-9\._]{1,20})/?$', views.CommunityView.as_view()),
    url(r'^graph/community/(?P<url_name>[a-zA-Z0-9\._]{1,20})/(?P<graph_name>[a-zA-Z0-9\._]{1,20})/?$',
        views.get_community_graph),
    url(r'^new_year_2018_game/scoreboards/?$', views.ScoreBoardViewSet.as_view({'get': 'list'})),
    url(r'^new_year_2018_game/top/?$', views.TopViewSet.as_view({'get': 'list'})),

    url(r'^pikabu_users/?$', views.PikabuUserViewSet.as_view({'get': 'list'})),
    # url(r'^pikabu_user/id/(?P<id>[0-9]{1,20})/?$', views.PikabuUserViewId.as_view()),
    # url(r'^pikabu_user/username/(?P<username>[a-zA-Z0-9\._]{1,20})/?$', views.PikabuUserViewUsername.as_view()),
]
