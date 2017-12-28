from django.conf.urls import url
from . import views

app_name = 'pikabu_new_year_18_game_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ugly_frontend/$', views.ugly_frontend, name='ugly_frontend'),
]
