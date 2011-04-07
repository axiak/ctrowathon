#!/usr/bin/python
import sys, os

d = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
if not d:
    d = '..'
print d

sys.path.insert(0, d)
os.chdir(d)

os.environ["DJANGO_SETTINGS_MODULE"] = "ctrowathon.settings"

from django.core.servers.fastcgi import runfastcgi

runfastcgi(outlog="/var/log/lighttpd/rowathon.log", daemonize="false",
           errlog="/var/log/lighttpd/rowathon.error.log", method="threaded", maxspare=5,
           maxchildren=10, minspare=2)


