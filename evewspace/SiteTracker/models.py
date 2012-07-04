from django.db import models
from django.contrib.auth.models import User
from evewspace.Map.models import Map, System

# Create your models here.

class Fleet(models.Model):
	"""Represents a SiteTracker fleet."""
	map = models.ForeignKey(Map, related_name="fleets")
	boss = models.ForeignKey(User, related_name="bossfleets")
	started = models.DateTimeField()
	ended = models.DateTimeField(blank=True, null=True)

	class Meta:
		permissions = (("can_sitetracker", "Use the Site Tracker system."),)

	def __unicode__(self):
		return u"Map: %s Boss: %s  Started: %s  Ended: %s" %(self.map.name, self.boss.name, self.started, self.ended)

class SiteType(models.Model):
	"""Represents a type of site that can be credited."""
	shortname = models.CharField(max_length=8)
	longname = models.CharField(max_length=80)
	# Defunct site types are maintained in the databse for relational purposes but can no longer be credited
	defunct = models.BooleanField()

	def __unicode__(self):
		return self.longname

class SiteRecord(models.Model):
	"""Represents the record of a site run."""
	fleet = models.ForeignKey(Fleet, related_name="sites")
	type = models.ForeignKey(SiteType, related_name="sitesrun")
	timestamp = models.DateTimeField(auto_now_add=True)
	system = models.ForeignKey(System, related_name="sitescompleted")
	boss = models.ForeignKey(User, related_name="sitescredited")
	fleetsize = models.IntegerField()
	
	def __unicode__(self):
		return u"System: %s Time: %s  Type: %s" % (self.system.name, self.timestamp, self.type.shortname)
	
class UserLog(models.Model):
	"""Represents a user's sitetracker log."""
	fleet = models.ForeignKey(Fleet, related_name="members")
	user = models.ForeignKey(User, related_name="sitetrackerlogs")
	jointime = models.DateTimeField(auto_now_add=True)
	leavetime = models.DateTimeField(null=True, blank=True)

class UserExclusion(models.Model):
	"""Represents sites that a User does not get credit for regardless of their UserLog."""
	user = models.ForeignKey(User, related_name="siteexclusions")
	site = models.ForeignKey(SiteRecord, related_name="userexclusions")

class UserInclusion(models.Model):
	"""Represents sites that a User does get credit for regardless of their UserLog."""
	user = models.ForeignKey(User, related_name="siteinclusions")
	site = models.ForeignKey(SiteRecord, related_name="userinclusions")

class ClaimPeriod(models.Model):
	"""Represents a claim period that Users can claim against."""
	starttime = models.DateTimeField()
	endtime = models.DateTimeField()
	name = models.CharField(max_length = 80)
	closetime = models.DateTimeField(blank=True, null=True)
	loothauledby = models.ForeignKey(User, related_name="loothauled", null=True, blank=True)
	lootsoldby = models.ForeignKey(User, related_name="lootsold", null=True, blank=True)
	class Meta:
		permissions = (("can_close_claims", "Close the claims period early."), 
				 ("can_reopen_claims", "Reopen the claims period."),
				 ("can_haul_loot", "Mark the claim period as hauled."),
				 ("can_sell_loot", "Mark the claim period as sold."),)
				 

	def __unicode__(self):
		return self.name

class Claim(models.Model):
	"""Represents a User's claim for a claim period."""
	period = models.ForeignKey(ClaimPeriod, related_name="claims")
	user = models.ForeignKey(User, related_name="claims")
	shareclaimed = models.FloatField()
	description = models.TextField()
	bonus = models.FloatField(blank=True, null=True)

class PayoutReport(models.Model):
	"""Represents a payout report and contains general information about the payout period."""
	period = models.ForeignKey(ClaimPeriod, related_name="reports")
	createdby = models.ForeignKey(User, related_name="payoutreports")
	grossprofit = models.BigIntegerField()
	datepaid = models.DateTimeField(blank=True, null=True)

class PayoutEntry(models.Model):
	"""Represents an entry in the payout report."""
	report = models.ForeignKey(PayoutReport, related_name="entries")
	user = models.ForeignKey(User, related_name="payouts")
	claim = models.ForeignKey(Claim, related_name="payout")
	iskshare = models.BigIntegerField()





