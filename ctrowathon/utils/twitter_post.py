import os

from twitter import Twitter, NoAuth, OAuth, read_token_file
from twitter.cmdline import CONSUMER_KEY, CONSUMER_SECRET

token_file = os.path.join(os.path.dirname(__file__), '.twitter_oauth')

oauth = OAuth(*read_token_file(token_file)
               + (CONSUMER_KEY, CONSUMER_SECRET))

twitter = Twitter(domain='api.twitter.com',
                  auth=oauth,
                  api_version='1')

__all__ = ('send_update',
           'get_updates',)

#HASH_TAG = '#crunchtimerowathon'
HASH_TAG = '#extremecouponing'

def send_update(message):
    random_tweet = message + " %s" % HASH_TAG
    twitter.statuses.update(status=random_tweet)

def get_updates():
    t = Twitter(domain='search.twitter.com')
    results = []
    for page in range(1, 2):
        results.extend(t.search(q=HASH_TAG, rpp=100, page=page)['results'])
    return results
