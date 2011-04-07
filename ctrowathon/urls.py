import os

from django.conf.urls.defaults import *
from django.conf import settings

from django.views import static

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', static.serve,
       {'document_root': os.path.join(settings.PROJECT_ROOT, 'public_html', 'media')}),
    (r'^$', 'row.views.main',),
    (r'^distance/?$', 'row.views.get_distance',),
)
