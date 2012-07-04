from django.db import models

# Core models contains models used across multiple apps

class MarketGroup(models.Model):
	"""A market group from the Eve SDD."""
	id          = models.BigIntegerField(primary_key=True, db_column='marketGroupID')
	name        = models.CharField(max_length = 100, null=True, blank=True, db_column='marketGroupName')
	parentgroup = models.ForeignKey("self", related_name="childgroups", blank=True, null=True, db_column='parentGroupID')
	description = models.CharField(max_length = 200, null=True, blank=True)
	hasTypes    = models.BooleanField()

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = 'invMarketGroups'

class Type(models.Model):
	"""A type from the Eve SDD invTypes table."""
	id          = models.BigIntegerField(primary_key=True, db_column='typeID')
	name        = models.CharField(max_length = 100, db_column='typeName')
	description = models.TextField(blank=True, null=True)
	volume      = models.FloatField(blank=True, null=True)
	marketgroup = models.ForeignKey(MarketGroup, related_name="types", db_column='marketGroupID')

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = 'invTypes'
	
class Region(models.Model):
	"""Core model for static region data"""

	id   = models.BigIntegerField(primary_key=True, db_column='regionID')
	name = models.CharField(max_length=100, db_column='regionName')
	x    = models.FloatField()
	y    = models.FloatField()
	z    = models.FloatField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'mapRegions'

class Constellation(models.Model):
	"""Core model for static constellation data, references Region"""
	id     = models.BigIntegerField(primary_key=True, db_column='constellationID')
	name   = models.CharField(max_length=100, db_column='constellationName')
	region = models.ForeignKey(Region, related_name='constellations', db_column='regionID')
	x      = models.FloatField()
	y      = models.FloatField()
	z      = models.FloatField()

	def __unicode__(self):
		return self.name

	class Meta:
		db_table = 'mapConstellations'

class SystemData(models.Model):
	"""Core model for static system data from the SDD, references Region and Constellation"""
	id       = models.BigIntegerField(primary_key=True, db_column='solarSystemID')
	name     = models.CharField(max_length=100, db_column='solarSystemName')
	constellation = models.ForeignKey(Constellation, related_name='systems', db_column='constellationID')
	region   = models.ForeignKey(Region, related_name='systems', db_column='regionID')
	x        = models.FloatField()
	y        = models.FloatField()
	z        = models.FloatField()
	security = models.FloatField()

	def __unicode__(self):
		return self.name
	
	class Meta:
		db_table = 'mapSolarSystems'

