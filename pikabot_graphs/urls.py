"""pikabot_graphs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^very_secret_admin_page_nobody_knows_this_address/', admin.site.urls),
    url(r'^', include('core.urls')),
    url(r'^communities/', include('communities_app.urls')),
    url(r'^pikabu_new_year_18_game_app/', include('pikabu_new_year_18_game_app.urls')),
    url(r'^', include('fakeadmin.urls')),
    url(r'^api/', include('api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static('angular/',
                          document_root=settings.ANGULAR_ROOT)
