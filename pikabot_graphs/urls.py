import os
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django
import core.views
import communities_app.views
import api.views


urlpatterns = [
    url(r'^', include('api.urls')),
    url(r'^secret_page_for_lactarius/$', communities_app.views.secret_page_for_lactarius,
        name='secret_page_for_lactarius'),
    url(r'^secret_page_for_l4rever/$', core.views.secret_page_for_l4rever,
        name='secret_page_for_l4rever'),

    url(r'^', include('fakeadmin.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        *static(settings.ANGULAR_STATIC_URL,
                document_root=settings.ANGULAR_STATIC_ROOT),
        url(r'^', api.views.angular_debug_url),
    ]
