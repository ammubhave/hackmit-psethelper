from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Party(models.Model):
    organizer = models.ForeignKey(User)
    class_for = models.CharField(max_length=64)
    description = models.TextField()
    short_description = models.TextField()
    location = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    latitude = models.IntegerField(default=-1)
    longitude = models.IntegerField(default=-1)
    def __unicode__(self):
        return self.class_for + ' ' + self.location + ' by ' + self.organizer.username

class PartyRequest(models.Model):
    party = models.ForeignKey(Party)
    requestor = models.ForeignKey(User)
    request_datetime = models.DateTimeField()
    approved = models.BooleanField(default=False)
    def __unicode__(self):
        return self.party.class_for + ' ' + self.requestor.username

