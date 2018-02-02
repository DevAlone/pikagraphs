from django.conf.urls import url
from . import views

app_name = 'pikabu_new_year_18_game_app'

urlpatterns = [
    url(r'^new_year_2018_game/scoreboards/?$', views.ScoreBoardViewSet.as_view({'get': 'list'})),
    url(r'^new_year_2018_game/top/?$', views.TopViewSet.as_view({'get': 'list'})),
]
