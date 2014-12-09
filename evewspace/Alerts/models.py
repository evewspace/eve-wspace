#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL

class SubscriptionGroup(models.Model):
    """Contians the definition for alert broadcast groups."""
    name = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=200)
    # A special alert group is one that cannot be individually joined or left.
    special = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='Subscription')

    class Meta:
        permissions = (("can_alert", "Use the alerts system."),
                         ("alert_admin", "Modify alert groups and rosters."),
                         ("can_ping_special", "Ping alert groups tagged special."),
                    )

    def __unicode__(self):
        return self.name

    def get_user_perms(self, user):
        """
        Returns a tuple of permissions for the subscription group as such:
            (can_broadcast, can_join)
        A user's highest permissions in both are returned and special gorups
        will always return can_join = False.
        """
        if self.special:
            user_perm = user.has_perm("Alerts.can_ping_special")
            return (user_perm, user_perm)
        can_join = False
        can_broadcast = False
        for group in user.groups.all():
            if self.group_permissions.filter(user_group=group).exists():
                perm = self.group_permissions.get(user_group=group)
                if perm.can_broadcast:
                    can_broadcast = True
                if perm.can_join:
                    can_join = True
        return (can_broadcast, can_join)


class Subscription(models.Model):
    """Mapping table that relates Users to their subscriped SubscriptionGroups."""
    group = models.ForeignKey(SubscriptionGroup)
    user = models.ForeignKey(User, related_name="alert_groups")


class SubscriptionGroupPermission(models.Model):
    """Mapping table that relates Groups to their permissions for SubscriptionGroups."""
    user_group = models.ForeignKey(Group, related_name="alert_groups")
    sub_group = models.ForeignKey(SubscriptionGroup, related_name="group_permissions")
    can_broadcast = models.BooleanField(default=False)
    can_join = models.BooleanField(default=False)
