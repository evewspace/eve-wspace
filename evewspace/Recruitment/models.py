from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Interest(models.Model):
	"""Represents an option for the 'What are you interests? question'"""
	name = models.CharField(max_length=100)

class Action(models.Model):
	"""Represents an action that can be taken on an application e.g Intel Ran"""
	name = models.CharField(max_length=100)

class Application(models.Model):
	"""Represents a recruitment application."""
	applicant = models.OneToOneField(User, related_name="application", primary_key=True)
	timestamp = models.DateTimeField()
	interests = models.ManyToManyField(Interest)
	killboard = models.CharField(max_length=100)
	#closetime = None indicates that the application is still open
	closetime = models.DateTimeField(blank=True, null=True)
	disposition = models.IntegerField(choices=((0,'Duplicate'), (1,'Accepted'), (2,'Rejected'), (3, 'Deferred')))
	intelclear = models.DateTimeField()
	standingsclear = models.BooleanField()

	def __unicode__(self):
		return 'Applicant: %s Status: %s' % (self.applicant.name, self.disposition)

class AppVote(models.Model):
	"""Represents a vote on an application"""
	application = models.ForeignKey(Application, related_name='votes')
	vote = models.ForeignKey(User, related_name='appvotes')
	disposition = models.IntegerField(choices=((1,'Accept',), (2,'Reject'), (3, 'Defer')))
	note = models.TextField()
	timestamp = models.DateTimeField()

class AppAction(models.Model):
	"""Represents an action taken on an application."""
	application = models.ForeignKey(Application, related_name='actions')
	action = models.ForeignKey(Action, related_name='instances')
	note = models.TextField()
	timestamp = models.DateTimeField()

class Interview(models.Model):
	"""Represents an interview for an application."""
	application = models.ForeignKey(Application, related_name='interviews')
	interviewer = models.ForeignKey(User, related_name='interviews')
	chatlog = models.TextField()
	timestamp = models.DateTimeField()

class AppQuestion(models.Model):
	"""Represents a question to be asked on the application."""
	question = models.CharField(max_length=255)

class AppResponse(models.Model):
	"""Represents a response to a custom application question."""
	application = models.ForeignKey(Application, related_name='responses')
	question = models.ForeignKey(AppQuestion, related_name='responses')
	response = models.TextField(blank=True, null=True)

class StandigsRequirement(models.Model):
	"""Represents a standing to be checked against applications."""
	entity = models.CharField(max_length=100)
	#If standing is null and we have a requirement record, we can interpret this as requiring no standing
	standing = models.FloatField(blank=True, null=True)
	entitytype = models.IntegerField(choices=((0,'Corporation'), (1,'Faction')))


