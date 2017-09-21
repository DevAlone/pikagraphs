from django.conf.urls import url

from . import views

fake_admin_regex = r'^admin/$|^wp-admin\.php$|^wp-login\.php$|^administrator/$'
fake_admin_regex += r'|^admin.php$|^login.php$|^cms/kernel/admin.php$'
fake_admin_regex += r'|^bitrix/admin/$|^manager/$|^login_form$|^modx/manager/$'
fake_admin_regex += r'|^administrator/index.php$'

app_name = 'fakeAdmin'
urlpatterns = [
    url(fake_admin_regex, views.fakeAdmin, name='fakeAdmin'),
]
