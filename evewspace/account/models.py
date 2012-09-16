from django.db import models
from django.contrib.auth.models import User, Group
from Map.models import Map, System
from django.db.models.signals import post_save
import pytz
import datetime
# Create your models here.

class PlayTime(models.Model):
    """PlayTime represents a choice of play times for use in several forms."""
    fromtime = models.TimeField()
    totime = models.TimeField()


class UserProfile(models.Model):
    """UserProfile defines custom fields tied to each User record in the Django auth DB."""
    user = models.ForeignKey(User, unique=True)
    jabberid = models.EmailField(blank=True, null=True)
    defaultmap = models.ForeignKey(Map, related_name = "defaultusers", blank=True, null=True)
    playtimes = models.ManyToManyField(PlayTime)
    currentsystem = models.ForeignKey(System, related_name="activepilots", blank=True, null=True)
    lastactive = models.DateTimeField()


class GroupProfile(models.Model):
    """GroupProfile defines custom fields tied to each Group record."""
    group = models.ForeignKey(Group, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)


def create_user_profile(sender, instance, created, **kwargs):
    """Handle user creation event and create a new profile to match the new user"""
    if created:
        UserProfile.objects.create(user=instance, lastactive=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))

post_save.connect(create_user_profile, sender=User)


def create_group_profile(sender, instance, created, **kwargs):
    """Handle group creation even and create a new group profile."""
    if created:
        GroupProfile.objects.create(group=instance)

post_save.connect(create_group_profile, sender=Group)
