from django.conf import settings
from Alerts.models import SubscriptionGroup
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL

class JabberSubscription(models.Model):
    """
    A registered User / Group combo for jabber.
    """
    user = models.ForeignKey(User, related_name='jabber_subs')
    group = models.ForeignKey(SubscriptionGroup, related_name='jabber_subs')

    def __unicode__(self):
        return "User %s  Group %s" % (self.user.username, self.group.name)


class JabberAccount(models.Model):
    """
    A jabber account to send messages to. JID is in user@host.tld format
    """
    user = models.ForeignKey(User, related_name='jabber_accounts')
    jid = models.CharField(max_length=200)

    def __unicode__(self):
        return "User: %s  JID: %s" % (self.user.username, self.jid)

class SlackChannel(models.Model):
    """
    Reference Slack channel to send messages to based on SubGroup name.
    """
    channel = models.CharField(max_length=50, null=False, unique=True)
    group = models.ForeignKey(SubscriptionGroup, related_name='slack_groups', null=False, unique=True)
    
    
    def __unicode__(self):
        return "Channel: %s Group: %s" % (self.channel, self.group.name)
    