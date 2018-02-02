from django.conf.urls import url
from . import views

app_name = 'communities_app'

urlpatterns = [
    url(r'^secret_page_for_lactarius/$', views.secret_page_for_lactarius,
        name='secret_page_for_lactarius'),
]
