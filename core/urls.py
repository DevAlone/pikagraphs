from django.conf.urls import url, include
from rest_framework import routers
from . import views
from pikabot_graphs import settings
import django
from django.views.generic import TemplateView
from django.views.generic import RedirectView

app_name = 'core'

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'user', views.UserView)

urlpatterns = [
    # url(r'^$', views.users, name='index'),
    # url(r'^users/$', views.users, name='users'),
    # url(r'^user/(?P<username>[a-zA-Z0-9\._]{1,20})/$', views.user, name='user'),
    # url(r'^secret_page_for_l4rever/$', views.secret_page_for_l4rever,
    #     name='secret_page_for_l4rever'),

    # url(r'^rest/', include(router.urls)),
]
