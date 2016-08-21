from __future__ import unicode_literals

import time
import random
from random_words import RandomWords



# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
# from random_words import RandomWords
from rest_framework.authtoken.models import Token


class Hrop(models.Model):

    user = models.ForeignKey(to=User, related_name='hrop', db_index=True, blank=False)
    time = models.DateTimeField(verbose_name='Time hroping', blank=False, db_index=True)
    period = models.PositiveIntegerField(blank=False, default=0)
    response_time = models.PositiveIntegerField(blank=False, default=0)
    intensity = models.PositiveIntegerField(blank=False, default=0)
    track_name = models.CharField(max_length=150, blank=True, default=None)
    volume_track = models.PositiveIntegerField(blank=False, default=0)

    class Meta:
        verbose_name = 'User hrop'

    def __unicode__(self):
        return 'Time: {} Response time: '.format(self.time, self.response_time)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        for day in xrange(62):
            timestamp = time.time() - day * 86400
            hrop_iter = random.randint(10, 64)

            for i in xrange(hrop_iter):
                date = {
                    "user": instance,
                    "response_time": random.randint(10, 70),
                    "intensity": random.randint(20, 95),
                    "track_name": ' '.join(RandomWords().random_words(count=4)),
                    "volume_track": random.randint(10, 100)
                }

                date.update({"period": date['response_time'] + random.randint(5, 15),})
                timestamp -= date['period']
                date.update({"time": timezone.now().fromtimestamp(timestamp)})

                Hrop.objects.create(**date)
