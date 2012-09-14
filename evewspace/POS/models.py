from django.db import models
from core.models import Type, Location
from Map.models import System
from django.contrib.auth.models import User

class Alliance(models.Model):
    """Represents an alliance, data pulled from api"""
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=100)
    executor = models.ForeignKey('Corporation', related_name='+')

    def __unicode__(self):
        return self.name

class Corporation(models.Model):
    """Represents a corporation, data pulled from api"""
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=100)
    alliance = models.ForeignKey(Alliance, null=True, blank=True, related_name='member_corps')
    member_count = models.IntegerField()

    def __unicode__(self):
        return self.name

class POS(models.Model):
    """Represents a POS somewhere in space."""
    #This location should always reference a moon from mapDenormalize
    #location = models.OneToOneField(Location, related_name="pos", primary_key=True)
    system = models.ForeignKey(System, related_name="poses")
    planet = models.IntegerField()
    moon   = models.IntegerField()
    towertype = models.ForeignKey(Type, related_name="inspace")
    corporation = models.ForeignKey(Corporation, related_name="poses")
    posname = models.CharField(max_length=100, blank=True, null=True)
    fitting = models.TextField(blank=True, null=True)
    #Using CCP's status codes here for sanity with API checks
    status = models.IntegerField(choices = ((0, 'Unanchored'), (1, 'Anchored'), (2, 'Onlining'), (3, 'Reinforced'), (4, 'Online')))

    #This should be the time the tower exits RF
    #TODO: add a validator to make sure this is only set if status = 3 (Reinforced)
    rftime = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField()

    def clean(self):
        from django.core.exceptions import ValidationError
        #XXX: commenting this out for now as it's in save() (and clean is
        #really there to catch errors in what has been input, not to handle
        #defaulting things) this should really be in only one of save or clean
        #if not self.posname:
        #       self.posname = self.towertype.name
        if rftime and status != 3:
            raise ValidationError("A POS cannot have an rftime unless it is reinforced")
        if not updated:
            import datetime
            updated = datetime.datetime.utcnow()


    def __unicode__(self):
        return self.location.name

    #overide save to implement posname defaulting to towertype.name
    def save(self, *args, **kwargs):
        if not self.posname:
            self.posname = self.towertype.name
        super(POS, self).save(*args, **kwargs)

class CorpPOS(POS):
    """A corp-controlled POS with manager and password data."""
    manager = models.ForeignKey(User, null=True, blank=True, related_name='poses')
    password = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    #Let's store the CCP Item ID for the tower here to make API lookup easier
    #If it is null, then we are not tracking this POS via API
    apiitemid = models.BigIntegerField(null=True, blank=True)

    class Meta:
        permissions = (('can_see_pos_pw', 'Can see corp POS passwords.'),
        ('can_see_all_pos', 'Sees all corp POSes regardless of manager.'),)

class POSApplication(models.Model):
    """Represents an application for a personal POS."""
    applicant = models.ForeignKey(User, null=True, blank=True, related_name='posapps')
    towertype = models.ForeignKey(Type, null=True, blank=True, related_name='posapps')
    residents = models.ManyToManyField(User)
    normalfit = models.TextField()
    siegefit = models.TextField()
    #Once it is approved, we will fill in these two to tie the records together
    approved = models.DateTimeField(blank=True, null=True)
    posrecord = models.ForeignKey(CorpPOS, blank=True, null=True, related_name='application')

    class Meta:
        permissions = (('can_close_pos_app', 'Can dispose of corp POS applications.'),)

    def __unicode__(self):
        return 'Applicant: %s  Tower: %s' % (self.applicant.username, self.towertype.name)

class POSVote(models.Model):
    """Represents a vote on a personal POS application."""
    application = models.ForeignKey(POSApplication, related_name='votes')
    voter = models.ForeignKey(User, related_name='posvotes')
    vote = models.IntegerField(choices=((0,'Deny'), (1, 'Approve'), (2, 'Abstain')))
