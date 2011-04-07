import simplejson

from django.http import HttpResponse
from django.views.generic import simple

from utils.twitter_post import *

from .distancethread import DistanceThread

DistanceThread.initialize()

def main(request):
    val = DistanceThread.singleton().get_distances()
    ctx = {}
    ctx['twitter_statuses'] = get_updates()[:10]
    response = simple.direct_to_template(request, 'mainrow.html', ctx)
    response['Refresh'] = 60
    return response


def get_distance(request):
    return HttpResponse(simplejson.dumps({'distance': DistanceThread.singleton().get_distance()[1]}),
                            mimetype="application/json")
