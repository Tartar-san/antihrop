import time
import random
from random_words import RandomWords
from hropapi.models import *
from django.utils import timezone


def fill(days, user):

    for day in xrange(days):
        timestamp = time.time() - day * 86400
        hrop_iter = random.randint(10, 64)

        for i in xrange(hrop_iter):
            date = {
                "user": user,
                "response_time": random.randint(10, 70),
                "intensity": random.randint(20, 95),
                "track_name": ' '.join(RandomWords().random_words(count=4)),
                "volume_track": random.randint(10, 100)
            }

            date.update({"period": date['response_time'] + random.randint(5, 15),})
            timestamp -= date['period']
            date.update({"time": timezone.now().fromtimestamp(timestamp)})

            Hrop.objects.create(**date)
