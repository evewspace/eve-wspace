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
from core.tasks import update_corporation
from core.utils import get_config
import cache_handler as handler

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User, Group
from datetime import datetime
import eveapi

import pytz
# Create your models here.


class APIKey(models.Model):
    """API Key object relates to User and contains key id, vcode, and validation information."""
    keyid = models.IntegerField()
    vcode = models.CharField(max_length=100)
    valid = models.BooleanField()
    lastvalidated = models.DateTimeField()
    access_mask = models.IntegerField()
    proxykey = models.CharField(max_length=100, null=True, blank=True)
    validation_error = models.CharField(max_length=255, null=True, blank=True)

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
    character_name = models.CharField(max_length=255, null=True, blank=True)

    def validate(self):
        """
        Validate a corp API key. Return False if invalid, True if valid.

        :returns: bool -- True if valid, False if invalid
        """
        api = eveapi.EVEAPIConnection(cacheHandler=handler)
        auth = api.auth(keyID=self.keyid, vCode=self.vcode)
        self.lastvalidated = datetime.now(pytz.utc)
        try:
            result = auth.account.APIKeyInfo()
        except eveapi.AuthenticationError:
            self.valid = False
            self.validation_error("Access Denied: Key not valid.")
            self.save()
            return False
        if result.key.type == u'Corporation':
            self.valid = True
            self.character_name = result.key.characters[0].characterName
            self.access_mask = result.key.accessMask
            self.corp = update_corporation(
                    result.key.characters[0].corporationID, sync=True)
            self.validation_error = True
            self.save()
            return True
        else:
            self.valid = False
            self.validation_error = "API Key is not a corporation key."
            return False


class MemberAPIKey(APIKey):
    """
    API key for individual member account.
    """
    user = models.ForeignKey(User, related_name="api_keys")

    def validate(self):
        """
        Validate a character API key. Return False if invalid, True
        if valid.

        :reutrns: bool -- True if valid, False if invalid
        """
        char_allowed = int(get_config("API_ALLOW_CHARACTER_KEY",
                None).value) == 1
        expire_allowed = int(get_config("API_ALLOW_EXPIRING_KEY",
                None).value) == 1
        api = eveapi.EVEAPIConnection(cacheHandler=handler)
        auth = api.auth(keyID=self.keyid, vCode=self.vcode)
        self.lastvalidated = datetime.now(pytz.utc)
        try:
            result = auth.account.APIKeyInfo()
        except eveapi.AuthenticationError:
            self.valid = False
            self.validation_error("Access Denied: Key not valid.")
            self.save()
            return False
        if result.key.type == u'Character' and not char_allowed:
            self.valid = False
            self.validation_error = ("API Key is a character key which is not "
                        "allowed by the administrator.")
            self.save()
            return False
        if result.key.expires and not expire_allowed:
            self.valid = False
            self.validation_error = ("API Key has an expiration date which is "
                        "not allowed by the administrator.")
            self.save()
            return False
        self.access_mask = result.key.accessMask
        corp_list = []
        access_error_list = []
        for character in result.key.characters:
            corp_list.append(character.corporationID)
        access_required = _build_access_req_list(self.user, corp_list)
        for access in access_required:
            if not access.requirement.key_allows(self.access_mask):
                access_error_list.append("Endpoint %s required but "
                        "not allowed." % access.requirement.call_name)
        if len(access_error_list):
            self.valid = False
            self.validation_error = ("The API Key does not meet "
                    "access requirements: \n\n")
            for x in access_error_list:
                self.validation_error = "%s \n %s" % (
                        self.validation_error, x)
            self.save()
            # Still try to get character details for security
            try:
                self.update_characters()
            except Exception:
                pass
            return False
        else:
            self.valid = True
            self.validation_error = ""
            self.save()
            self.update_characters()
            return True

    def update_characters(self):
        api = eveapi.EVEAPIConnection(cacheHandler=handler)
        auth = api.auth(keyID=self.keyid, vCode=self.vcode)
        key_info = auth.account.APIKeyInfo()
        for character in key_info.key.characters:
            char_info = auth.eve.CharacterInfo(
                    characterID=character.characterID)
            char_name = char_info.characterName
            corp = char_info.corporation
            if 'alliance' in char_info.__dict__:
                alliance = char_info.alliance
            else:
                alliance = "None"
            if 'lastKnownLocation' in char_info.__dict__:
                location = char_info.lastKnownLocation
            else:
                location = "Unknown"
            if 'shipName' in char_info.__dict__:
                log_enabled = True
                lastshipname = char_info.shipName
                lastshiptype = char_info.shipTypeName
            else:
                log_enabled = False
                lastshipname = "Unknown"
                lastshiptype = "Unknown"

            api_char = APICharacter.objects.get_or_create(
                    charid=char_info.characterID, defaults={
                        'apikey': self, 'name': char_name})[0]
            APICharacter.objects.filter(
                    charid=char_info.characterID).update(
                            apikey=self, name=char_name,
                            corp=corp, alliance=alliance,
                            location=location, lastshipname=lastshipname,
                            lastshiptype=lastshiptype, visible=True)
            if log_enabled:
                # Log this character data for security reference
                APIShipLog(character=api_char,
                        timestamp=datetime.now(pytz.utc),
                        shiptype=lastshiptype,
                        shipname=lastshipname,
                        location=location).save()


def _build_access_req_list(user, corp_list):
    """
    :param: user -- User object
    :param: corp_list -- List of corporation IDs to consider
    :returns: list(APIAccessType) -- List of API Access Types required
    """
    result = []
    # Corp-wide requirements
    for access in APIAccessRequirement.objects.filter(
            corps_required__in=corp_list,
            groups_required__isnull=True):
        result.append(access)
    # Group-wide requirements
    for access in APIAccessRequirement.objects.filter(
            groups_required__in=user.groups.all(),
            corps_required__isnull=True):
        if access not in result:
            result.append(access)
    # Group-Corp requirements
    for access in APIAccessRequirement.objects.filter(
            groups_required__in=user.groups.all(),
            corps_required__in=corp_list):
        if access not in result:
            result.append(access)
    return result


class APICharacter(models.Model):
    """API Character contains the API security information of a single character."""
    apikey = models.ForeignKey(APIKey, related_name="characters")
    charid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    corp = models.CharField(max_length=100, blank=True, null=True)
    alliance = models.CharField(max_length=100, blank=True, null=True)
    lastshipname = models.CharField(max_length=100, blank=True, null=True)
    lastshiptype = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    visible = models.NullBooleanField()

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

    def key_allows(self, key_mask):
        """
        Returns True if the provided key allows this APIAccessType.
        """
        return (self.call_mask & key_mask) == self.call_mask

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
    corps_required  = models.ManyToManyField(Corporation,
            related_name="api_requirements", null=True)
    requirement = models.ForeignKey(APIAccessType,
            related_name="required_by")
    groups_required = models.ManyToManyField(Group, null=True,
            related_name="api_requirements")
