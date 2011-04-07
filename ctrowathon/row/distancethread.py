import threading
import collections
import fcntl
import datetime
import subprocess
import os
import random
import functools

from utils.twitter_post import *

__all__ = ('DistanceThread',)

alerts = []

def distance_alert(method):
    alerts.append(method)
    return method

class DistanceThread(threading.Thread):
    distance = 0
    
    def __init__(self):
        threading.Thread.__init__(self, name="distanceThread")
        self.setDaemon(True)
        self.distance = 0
        self._lock = threading.Lock()
        self._queue = collections.deque([], 1000)

    def get_distance(self):
        with self._lock:
            return self._queue[0]

    def get_distances(self):
        with self._lock:
            result = tuple(self._queue)
        return result

    @classmethod
    def singleton(cls):
        return getattr(cls, '_singleton', None)

    @classmethod
    def initialize(cls):
        if getattr(cls, '_singleton', None):
            return
        cls._singleton = True
        cls._singleton = cls()
        cls._singleton.start()

    def run(self):
        row_cmd = os.path.join(os.path.dirname(__file__), '..', 'cmd', 'row.py')
        lock_file = open('/tmp/row_lock', 'w')
        fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
        while True:
            p = subprocess.Popen([row_cmd], stdout=subprocess.PIPE, shell=True)
            while True:
                if p.poll():
                    break
                value = p.stdout.readline().strip()
                try:
                    value = value.split()
                    value = float(value[0]), float(value[1])
                except:
                    continue
                with self._lock:
                    self._queue.appendleft((datetime.datetime.now(), value[0], value[1]))
                    vals = tuple(self._queue)
                for alert in alerts:
                    alert(vals)


@distance_alert
def static_boundary(values):
    if len(values) < 2:
        return
    if (int(values[0][1]) / 10000) > (int(values[1][1]) / 10000):
        value = int(values[0][1]) / 1000
        send_alert("%s kilometers down." % value)

def send_alert(alert_text):
    text_helpers = ('Way to go!',
                    'Keep going!',
                    )
    send_update("%s %s" % (alert_text, random.choice(text_helpers)))
