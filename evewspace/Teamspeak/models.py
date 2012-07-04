from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class TeamspeakServer(models.Model):
	"""Stores teamspeak server configuration."""
	host = models.CharField(max_length=100)
	queryuser = models.CharField(max_length=100)
	querypass = models.CharField(max_length=100)
	queryport = models.IntegerField()
	voiceport = models.IntegerField()
	# If enforcegroups = True, any TS users who do not have a GroupMap entry will have no groups
	enforcegroups = models.BooleanField()
	# If enforceusers = True, any TS users without a Django user mapping will be removed
	enforeceusers = models.BooleanField()

class GroupMap(models.Model):
	"""Maps Django user groups to Teamspeak groups."""
	tsserver = models.ForeignKey(TeamspeakServer, related_name="groupmaps")
	usergroup = models.ForeignKey(Group, related_name="teamspeakgroups")
	tsgroup = models.CharField(max_length=100)

