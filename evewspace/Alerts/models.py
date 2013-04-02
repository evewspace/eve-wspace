#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

class SubscriptionGroup(models.Model):
    """Contians the definition for alert broadcast groups."""
    name = models.CharField(max_length=64, unique=True)
    desc = models.CharField(max_length=200)
    # A special alert group is one that cannot be individually joined or left.
    special = models.BooleanField()
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
    can_broadcast = models.BooleanField()
    can_join = models.BooleanField()
