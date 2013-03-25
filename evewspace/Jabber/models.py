from django.contrib.auth.models import User
from Alerts.models import SubscriptionGroup
from django.db import models

# Create your models here.

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

