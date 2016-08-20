from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

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