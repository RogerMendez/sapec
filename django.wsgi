import os, sys

sys.path.append("E:/Django/sapec")
os.environ['DJANGO_SETTINGS_MODULE'] = 'sapec.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()