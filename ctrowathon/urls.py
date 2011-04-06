import os

from django.conf.urls.defaults import *
from django.conf import settings

from django.views.static import serve

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', serve,
       {'document_root': os.path.join(settings.PROJECT_ROOT, 'public_html', 'media')}),
    # Example:
    # (r'^ctrowathon/', include('ctrowathon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
