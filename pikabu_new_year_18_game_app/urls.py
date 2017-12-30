from django.conf.urls import url
from . import views

app_name = 'pikabu_new_year_18_game_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^avatars_only/$', views.avatars_only, name='avatars_only'),
    url(r'^ugly_frontend/$', views.ugly_frontend, name='ugly_frontend'),
    url(r'^get_score_items/(?P<from_timestamp>[0-9]{1,20})/(?P<to_timestamp>[0-9]{1,20})/$',
        views.get_score_items, name='get_score_items'),
]
