import threading
import collections
import datetime
import subprocess
import os

__all__ = ('DistanceThread',)

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
        while True:
            p = subprocess.Popen([row_cmd], stdout=subprocess.PIPE, shell=True)
            while True:
                if p.poll():
                    break
                value = p.stdout.readline().strip()
                try:
                    value = float(value)
                except:
                    continue
                with self._lock:
                    self._queue.appendleft((datetime.datetime.now(), value))
