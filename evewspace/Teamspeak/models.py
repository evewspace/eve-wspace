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

# Create your models here.

class TeamspeakServer(models.Model):
    """Stores teamspeak server configuration."""
    host = models.CharField(max_length=100)
    queryuser = models.CharField(max_length=100)
    querypass = models.CharField(max_length=100)
    queryport = models.IntegerField()
    voiceport = models.IntegerField()
    # If enforcegroups = True, any TS users who do not have a GroupMap entry will have no groups
    enforcegroups = models.BooleanField(default=False)
    # If enforceusers = True, any TS users without a Django user mapping will be removed
    enforeceusers = models.BooleanField(default=False)

    @classmethod
    def create(cls,host,queryuser,querypass,queryport,voiceport):
        ts3= cls(host=host,queryuser=queryuser,querypass=querypass,queryport=queryport,voiceport=voiceport)
        return ts3

    class Meta:
        permissions = (('ts_admin', 'Can administer Teamspeak settings'),
                       ('ts_see_online', 'Can see online TS users'),
                       )

class GroupMap(models.Model):
    """Maps Django user groups to Teamspeak groups."""
    tsserver = models.ForeignKey(TeamspeakServer, related_name="groupmaps")
    usergroup = models.ForeignKey(Group, related_name="teamspeakgroups")
    tsgroup = models.CharField(max_length=100)

