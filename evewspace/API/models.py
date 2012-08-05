from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class APIKey(models.Model):
	"""API Key object relates to User and contains key id, vcode, and validation information."""
	user = models.ForeignKey(User, related_name = "apikeys")
	keyid = models.IntegerField()
	vcode = models.CharField(max_length = 100)
	valid = models.BooleanField()
	lastvalidated = models.DateTimeField()
	proxykey = models.CharField(max_length = 100, null=True, blank=True)

	class Meta:
		permissions = (("add_keys", "Add API keys for others."), 
				 ("purge_keys", "Purge API Keys."), 
				 ("audit_keys", "View Users with no API keys assigned."),
				 ("key_required", "Nag if no API key registered."))
	
	def __unicode__(self):
		"""Return key ID as unicode representation."""
		return self.keyid


class APICharacter(models.Model):
	"""API Character contains the API information of a single character."""
	apikey = models.ForeignKey(APIKey, related_name = "characters")
	charid = models.BigIntegerField()
	name = models.CharField(max_length = 100)
	corp = models.CharField(max_length = 100)
	alliance = models.CharField(max_length = 100)
	lastshipname = models.CharField(max_length = 100)
	lastshiptype = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)
	visible = models.BooleanField()

	class Meta:
		permissions = (("view_limited_data", "View limited character API."), 
				 ("view_full_data", "View full character API."),)
				 

	def __unicode__(self):
		"""Return character name as unicode representation."""
		return self.name

class APIShipLog(models.Model):
	"""API Ship Log contains a timestamped record of a ship being flown by a character."""
	character = models.ForeignKey(APICharacter, related_name = "shiplogs")
	timestamp = models.DateTimeField()
	shiptype = models.CharField(max_length = 100)
	shipname = models.CharField(max_length = 100)
	location = models.CharField(max_length = 100)

	class Meta:
		permissions = (("view_shiplogs", "View API ship log entries."),)

	def __unicode__(self):
		"""Return ship type as unicode representation."""
		return self.shiptype

class APICachedDocument(models.Model):
	"""APICachedDocument represents a chached API document for our cache handler."""
	host = models.CharField(max_length = 100)
	params = models.CharField(max_length = 200)
	path = models.CharField(max_length = 100)
	xml = models.TextField()
	cacheduntil = models.DateTimeField()

	class Meta:
		permissions = (("clear_api_cache", "Clear the API document cache."),)

	def __unicode__(self):
		"""Return path name as unicode representation."""
		return self.path
