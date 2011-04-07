import os
import sys

python_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if python_path not in sys.path:
    sys.path.append(python_path)
    sys.path.append(os.path.join(python_path, 'ctrowathon'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ctrowathon.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
