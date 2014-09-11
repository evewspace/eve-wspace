from django.db import models
from django.conf import settings
from Alerts.models import SubscriptionGroup

User = settings.AUTH_USER_MODEL

class SlackChannel(models.Model):
    """
    Reference Slack channel to send messages to based on SubGroup name.
    """
    channel = models.CharField(max_length=50, null=False, unique=True)
    token = models.CharField(max_length=50, null=False)
    group = models.ForeignKey(SubscriptionGroup, related_name='slack_groups', null=False, unique=True)


    def __unicode__(self):
        return "Channel: %s Group: %s" % (self.channel, self.group.name)

