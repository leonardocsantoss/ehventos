from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from view import index

urlpatterns = patterns('',
    # Example:
    # (r'^base/', include('base.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', index, name="index"),
    # Uncomment the next line to enable the admin:
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    (r'^', include('ehv.urls')),
    (r'^usuario/', include('account.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

)

if settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    )
