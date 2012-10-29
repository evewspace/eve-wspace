from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
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

    def update_location(self, system):
        """
        updates the current location and last active timestamp for this user
        """
        self.currentsystem = system
        self.lastactive = datetime.datetime.now(pytz.utc)
        self.save()


class GroupProfile(models.Model):
    """GroupProfile defines custom fields tied to each Group record."""
    group = models.ForeignKey(Group, related_name='profile', unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    regcode = models.CharField(max_length=64, blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    """Handle user creation event and create a new profile to match the new user"""
    if created:
        UserProfile.objects.create(user=instance, lastactive=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))

post_save.connect(create_user_profile, sender=User)


def create_group_profile(sender, instance, created, **kwargs):
    """Handle group creation event and create a new group profile."""
    if created:
        GroupProfile.objects.create(group=instance)

post_save.connect(create_group_profile, sender=Group)


class RegistrationForm(UserCreationForm):
    """Extends the django registration form to add fields."""
    username = forms.CharField(max_length=30, label="Character Name", help_text="<br /> This will act as your username as well.")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password:")
    regcode = forms.CharField(max_length=64, label="Registration Code")

