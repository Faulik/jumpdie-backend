from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns(
    '',
    url(r'^$', 'djchat.views.home'),
    url(r'^control/', include(admin.site.urls)),
    url(r'^api/v1/accounts/', include('registration.backends.default.urls'))
)

urlpatterns += staticfiles_urlpatterns()
