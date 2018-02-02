from django.conf.urls import url
from . import views
app_name = 'core'

urlpatterns = [
    url(r'^secret_page_for_l4rever/$', views.secret_page_for_l4rever,
        name='secret_page_for_l4rever'),
]
