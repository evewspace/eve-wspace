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

class JabberGroup(models.Model):
    """Contians the definition for Jabber broadcast groups."""
    name = models.CharField(max_length=64)
    desc = models.CharField(max_length=200)
    # A special jabber group is one that cannot be individually joined or left.
    special = models.BooleanField()

    class Meta:
        permissions = (("can_jabber", "Use the jabber system."),
                         ("jabber_admin", "Modify jabber groups and rosters."),)

    def __unicode__(self):
        return self.name


class JabberGroupMember(models.Model):
    """Mapping table that relates Users to their subscriped JabberGroups."""
    group = models.ForeignKey(JabberGroup, related_name="members")
    user = models.ForeignKey(User, related_name="jabber_groups")


class JabberGroupPermissions(models.Model):
    """Mapping table that relates Groups to their permissions for JabberGroups."""
    usergroup = models.ForeignKey(Group, related_name="jabber_groups")
    jabbergroup = models.ForeignKey(JabberGroup, related_name="group_permissions")
    canbroadcast = models.BooleanField()
    canjoin = models.BooleanField()

