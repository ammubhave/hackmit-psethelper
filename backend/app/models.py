from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Party(models.Model):
    organizer = models.ForeignKey(User)
    class_for = models.CharField(max_length=64)
    short_description = models.TextField()
    description = models.TextField()
    location = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    latitude = models.IntegerField(default=-1)
    longitude = models.IntegerField(default=-1)

class PartyRequest(models.Model):
    party = models.ForeignKey(Party)
    requestor = models.ForeignKey(User)
    request_datetime = models.DateTimeField()
    approved = models.BooleanField(default=False)

