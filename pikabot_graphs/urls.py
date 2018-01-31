import os
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django
import core.views
import api.views


urlpatterns = [
    url(r'^', include('core.urls')),
    url(r'^api/', include('api.urls')),
    # url(r'^very_secret_admin_page_nobody_knows_this_address/', admin.site.urls),
    # url(r'^communities/', include('communities_app.urls')),
    # url(r'^pikabu_new_year_18_game_app/', include('pikabu_new_year_18_game_app.urls')),
    # url(r'^', include('fakeadmin.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        *static(settings.ANGULAR_STATIC_URL,
                document_root=settings.ANGULAR_STATIC_ROOT),
        url(r'^', api.views.angular_debug_url),
    ]
