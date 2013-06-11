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
from core.models import Corporation

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
# Create your models here.


class APIKey(models.Model):
    """API Key object relates to User and contains key id, vcode, and validation information."""
    keyid = models.IntegerField()
    vcode = models.CharField(max_length=100)
    valid = models.BooleanField()
    lastvalidated = models.DateTimeField()
    proxykey = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        permissions = (("add_keys", "Add API keys for others."),
                         ("purge_keys", "Purge API Keys."),
                         ("audit_keys", "View Users with no API keys assigned."),
                         ("key_required", "Nag if no API key registered."))

    def __unicode__(self):
        """Return key ID as unicode representation."""
        return self.keyid


class CorpAPIKey(APIKey):
    """
    Corp API keys used for corp stuff.
    """
    corp = models.ForeignKey(Corporation, related_name="api_keys")


class MemberAPIKey(APIKey):
    """
    API key for individual member account.
    """
    user = models.ForeignKey(User, related_name="api_keys")


class APICharacter(models.Model):
    """API Character contains the API security information of a single character."""
    apikey = models.ForeignKey(APIKey, related_name="characters")
    charid = models.BigIntegerField()
    name = models.CharField(max_length=100)
    corp = models.CharField(max_length=100)
    alliance = models.CharField(max_length=100)
    lastshipname = models.CharField(max_length=100)
    lastshiptype = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    visible = models.BooleanField()

    class Meta:
        permissions = (("view_limited_data", "View limited character API."),
                         ("view_full_data", "View full character API."),)

    def __unicode__(self):
        """Return character name as unicode representation."""
        return self.name


class APIShipLog(models.Model):
    """API Ship Log contains a timestamped record of a ship being flown by a character."""
    character = models.ForeignKey(APICharacter, related_name="shiplogs")
    timestamp = models.DateTimeField()
    shiptype = models.CharField(max_length=100)
    shipname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        permissions = (("view_shiplogs", "View API ship log entries."),)

    def __unicode__(self):
        """Return ship type as unicode representation."""
        return self.shiptype


class APIAccessGroup(models.Model):
    """Stores the access mask access groups from the CallList call."""
    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(max_length=255)
    group_description = models.TextField(blank=True, null=True)


class APIAccessType(models.Model):
    """Stores the access masks and types pulled from the CallList call."""
    call_type = models.IntegerField(choices=[(1,'Character'),
                                             (2,'Corporation')])
    call_name = models.CharField(max_length=255)
    call_description = models.TextField(blank=True, null=True)
    call_group = models.ForeignKey(APIAccessGroup,
            related_name="calls")
    call_mask = models.IntegerField()

    def is_required_for_user(self, user, corp):
        """
        Returns True if the APIAccessType is required for this user / corp.
        Also returns True if the APIAccessType is required for any of the
        user's groups.
        """
        return APIAccessRequirement.objects.filter(Q(corp=corp) |
                        Q(groups_required__in=user.groups.all()),
                        requirement=self).exists()


class APIAccessRequirement(models.Model):
    """Stores the required access for member API keys for a corp."""
    corp = models.ForeignKey(Corporation, related_name="api_requirements")
    requirement = models.ForeignKey(APIAccessType, related_name="required_by")
    groups_required = models.ManyToManyField(Group, null=True)
