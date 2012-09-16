from django.db import models
from django.contrib.auth.models import User, Group
from core.models import SystemData
from django.forms import ModelForm

# Create your models here.

class WormholeType(models.Model):
    """Stores the permanent information on wormhole types.
    Any changes to this table should be made with caution.

    """
    name = models.CharField(max_length = 4, unique = True)
    maxmass = models.BigIntegerField()
    jumpmass = models.BigIntegerField()
    lifetime = models.IntegerField()
    target = models.CharField(max_length = 15)

    def __unicode__(self):
        """Returns Wormhole ID as unicode representation."""
        return self.name


class System(SystemData):
    """Stores the permanent record of a solar system. 
    This table should not have rows added or removed through Django.

    """
    sysclass_choices = ((1, "C1"), (2, "C2"), (3, "C3"), (4, "C4"), (5, "C5"),
            (6, "C6"), (7, "High Sec"), (8, "Low Sec"), (9, "Null Sec"))
    sysclass = models.IntegerField(choices = sysclass_choices)
    occupied = models.TextField(blank = True)
    info = models.TextField(blank = True)
    lastscanned = models.DateTimeField()

    def __unicode__(self):
        """Returns name of System as unicode representation"""
        return self.name


class KSystem(System):
    sov = models.CharField(max_length = 100)


class WSystem(System):
    static1 = models.ForeignKey(WormholeType, blank=True, null=True, related_name="primary_statics")
    static2 = models.ForeignKey(WormholeType, blank=True, null=True, related_name="secondary_statics")


class Map(models.Model):
    """Stores the maps available in the map tool. root relates to System model."""
    name = models.CharField(max_length = 100, unique = True)
    root = models.ForeignKey(System, related_name="root")
    # Maps with explicitperms = True require an explicit permission entry to access.
    explicitperms = models.BooleanField()

    class Meta:
        permissions = (("map_unrestricted", "Do not require excplicit access to maps."),)

    def __unicode__(self):
        """Returns name of Map as unicode representation."""
        return self.name


class MapSystem(models.Model):
    """Stores information regarding which systems are active in which maps at the present time."""
    map = models.ForeignKey(Map, related_name="systems")
    system = models.ForeignKey(System, related_name="maps")
    friendlyname = models.CharField(max_length = 10)
    interesttime = models.DateTimeField(null=True, blank=True)
    parentsystem = models.ForeignKey('self', related_name="childsystems", 
            null=True, blank=True)

    def __unicode__(self):
        return "system %s in map %s" % (self.system.name, self.map.name)


class Wormhole(models.Model):
    """An instance of a wormhole in a  map. 
    Wormhole have a 'top' and a 'bottom', the top refers to the 
    side that is found first (and the bottom is obviously the other side)

    """
    map = models.ForeignKey(Map, related_name='wormholes')
    top = models.ForeignKey(MapSystem, related_name='child_wormholes')
    top_type = models.ForeignKey(WormholeType, related_name='+')
    top_bubbled = models.NullBooleanField(null=True, blank=True)
    bottom = models.ForeignKey(MapSystem, null=True, related_name='parent_wormholes') 
    bottom_type = models.ForeignKey(WormholeType, related_name='+')
    bottom_bubbled = models.NullBooleanField(null=True, blank=True)
    time_status = models.IntegerField(choices = ((0, "Fine"), (1, "End of Life")))
    mass_status = models.IntegerField(choices = ((0, "No Shrink"), 
        (1, "First Shrink"), (2, "Critical")))


class SignatureType(models.Model):
    """Stores the list of possible signature types for the map tool. 
    Custom signature types may be added at will.

    """
    shortname = models.CharField(max_length = 6)
    longname = models.CharField(max_length = 100)
    # sleepersite and escalatable are used to track wormhole comabt sites.
    # sleepersite = true should give a "Rats cleared" option
    # escalatable = true should cause escalation tracking to kick in in C5/6
    sleeprsite = models.BooleanField()
    escalatable = models.BooleanField()

    def __unicode__(self):
        """Returns short name as unicode representation"""
        return self.shortname


class Signature(models.Model):
    """Stores the signatures active in all systems. Relates to System model."""
    system = models.ForeignKey(System, related_name="signatures")
    sigtype = models.ForeignKey(SignatureType, related_name="sigs")
    sigid = models.CharField(max_length = 10)
    updated= models.DateTimeField()
    #ratscleared and lastescalated are used to track wormhole combat sites.
    #ratscleared is the DateTime that sleepers were cleared initially
    #lastescalated is the last time the site was escalated (if applicable)
    ratscleared = models.DateTimeField(null=True, blank=True)
    lastescalated = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        """Returns sig ID as unicode representation"""
        return self.sigid


class MapPermission(models.Model):
    """Relates a user group to it's map permissions. Non-restricted groups will have change access to all maps."""
    group = models.ForeignKey(Group, related_name="mappermissions")
    map = models.ForeignKey(Map, related_name="grouppermissions")
    access = models.IntegerField(choices=((0,'No Access'),
        (1,'View Only'), (2,'View / Change')))


class MapLog(models.Model):
    """Represents an action that has taken place on a map (e.g. adding a signature). 
    This is used for pushing updates since last page load to clients.

    """
    map = models.ForeignKey(Map, related_name="logentries")
    user = models.ForeignKey(User, related_name="maplogs")
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)

    def __unicode__(self):
        return "Map: %s  User: %s  Action: %s  Time: %s" % (self.map.name, self.user.username, 
                self.action, self.timestamp)

# Model Forms
class MapForm(ModelForm):
    class Meta:
        model = Map
