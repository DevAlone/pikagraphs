from django.conf.urls import url, include
from rest_framework import routers
from . import views
from pikabot_graphs import settings
import django
from django.views.generic import TemplateView

app_name = 'core'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # url(r'^$', views.users, name='index'),
    # url(r'^users/$', views.users, name='users'),
    # url(r'^user/(?P<username>[a-zA-Z0-9\._]{1,20})/$', views.user, name='user'),
    # url(r'^secret_page_for_l4rever/$', views.secret_page_for_l4rever,
    #     name='secret_page_for_l4rever'),
    # url(r'^inline.bundle.js$', TemplateView.as_view(template_name='inline.bundle.js')),
    # url(r'^polyfills.bundle.js$', TemplateView.as_view(template_name='polyfills.bundle.js')),
    # url(r'^styles.bundle.js$', TemplateView.as_view(template_name='styles.bundle.js')),
    # url(r'^vendor.bundle.js$', TemplateView.as_view(template_name='vendor.bundle.js')),
    # url(r'^main.bundle.js$', TemplateView.as_view(template_name='main.bundle.js')),
    # url(r'^.bundle.js$', TemplateView.as_view(template_name='index.html')),
    # url(r'^.bundle.js$', TemplateView.as_view(template_name='index.html')),
    # url(r'^.bundle.js$', TemplateView.as_view(template_name='index.html')),


    url(r'^OK/$', views.OK, name='OK'),
    url(r'^rest/', include(router.urls)),
]

