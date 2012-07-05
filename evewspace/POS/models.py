from django.db import models
from evewspace.core.models import SystemData, Type, StarbaseResource, StarbaseResourcePurpose, Location
from django.contrib.auth.models import User
# Create your models here.

class POS(models.Model):
	"""Represents a POS somewhere in space."""
	#This location should always reference a moon from mapDenormalize
	location = models.ForeignKey(Location, related_name="pos", primary_key=True)
	towertype = models.ForeignKey(Type, related_name="inspace")
	#Store this data (hopefully auto-populated from API by view) because it is expensive to get and we might not always be able to auto-resolve
	corpname = models.CharField(max_length=100)
	corpticker = models.CharField(max_length=10)
	alliancename = models.CharField(max_length=100)
	allianceticker = models.CharField(max_length=10)
	corpid = models.BigIntegerField(null=True, blank=True)
	#If posname is null, views should return towertype.name
	posname = models.CharField(max_length=100, null=True, blank=True)
	fitting = models.TextField()
	#Using CCP's status codes here for sanity with API checks
	status = models.IntegerField(choices = ((0, 'Unanchored'), (1, 'Anchored'), (2, 'Onlining'), (3, 'Reinforced'), (4, 'Online')))

	#This should be the time the tower exits RF
	rftime = models.DateTimeField(null=True, blank=True)
	updated = models.DateTimeField()

	def __unicode__(self):
		return self.location.name

class CorpPOS(POS):
	"""A corp-controlled POS with manager and password data."""
	manager = models.ForeignKey(User, null=True, blank=True, related_name='poses')
	password = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)

	class Meta:
		permissions = (('can_see_pos_pw', 'Can see corp POS passwords.'),)

class POSApplication(models.Model):
	"""Represents an application for a personal POS."""
	applicant = models.ForeignKey(User, null=True, blank=True, related_name='posapps')
	towertype = models.ForeignKey(Type, null=True, blank=True, related_name='posapps')
	normalfit = models.TextField()
	siegefit = models.TextField()
	#Once it is approved, we will fill in these two to tie the records together
	approved = models.DateTimeField(blank=True, null=True)
	posrecord = models.ForeignKey(CorpPOS, blank=True, null=True, related_name='application')
	
	class Meta:
		permissions = (('can_close_pos_app', 'Can dispose of corp POS applications.'),)
	
	def __unicode__(self):
		return 'Applicant: %s  Tower: %s' % (self.applicant.name, self.towertype.name)

class POSVotes(models.Model):
	"""Represents a vote on a personal POS application."""
	application = models.ForeignKey(POSApplication, related_name='votes')
	voter = models.ForeignKey(User, related_name='posvotes')
	vote = models.IntegerField(choices=((0,'Deny'), (1, 'Approve'), (2, 'Abstain')))

