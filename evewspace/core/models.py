from django.db import models
# Core models contains models used across multiple apps

class MarketGroup(models.Model):
    """A market group from the Eve SDD."""
    id = models.IntegerField(primary_key=True, db_column='marketGroupID')
    name = models.CharField(max_length = 100, null=True, blank=True, 
            db_column='marketGroupName')
    parentgroup = models.ForeignKey("self", related_name="childgroups", 
            blank=True, null=True, db_column='parentGroupID')
    description = models.CharField(max_length = 200, null=True, blank=True)
    hasTypes = models.BooleanField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'invMarketGroups'


class Type(models.Model):
    """A type from the Eve SDD invTypes table."""
    id = models.IntegerField(primary_key=True, db_column='typeID')
    name = models.CharField(max_length = 100, db_column='typeName')
    description = models.TextField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    marketgroup = models.ForeignKey(MarketGroup, related_name="types",
            db_column='marketGroupID')
    published = models.BooleanField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'invTypes'


class Region(models.Model):
    """Core model for static region data"""

    id   = models.IntegerField(primary_key=True, db_column='regionID')
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
    id = models.IntegerField(primary_key=True, db_column='constellationID')
    name = models.CharField(max_length=100, db_column='constellationName')
    region = models.ForeignKey(Region, related_name='constellations', 
            db_column='regionID')
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mapConstellations'


class SystemData(models.Model):
    """Core model for static system data from the SDD, references Region and Constellation"""
    id = models.IntegerField(primary_key=True, db_column='solarSystemID')
    name = models.CharField(max_length=100, db_column='solarSystemName')
    constellation = models.ForeignKey(Constellation, related_name='systems',
            db_column='constellationID')
    region = models.ForeignKey(Region, related_name='systems', db_column='regionID')
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    security = models.FloatField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mapSolarSystems'


class StarbaseResourcePurpose(models.Model):
    """Core model for SDD invControlTowerResourcePurpose table."""
    purpose = models.IntegerField(primary_key=True)
    purposeText = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.purposeText

    class Meta:
        db_table = 'invControlTowerResourcePurposes'


class StarbaseResource(models.Model):
    """Core model for SDD invStarbaseResources table. Maps tower types 
    to their fuel"""
    towerType = models.ForeignKey(Type, related_name='posesfueled', 
            db_column='controlTowerTypeID', primary_key=True)
    resourceType = models.ForeignKey(Type, related_name='posfuel', 
            db_column='resourceTypeID')
    purpose = models.ForeignKey(StarbaseResourcePurpose, related_name='usedby',
            db_column='purpose', blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True, db_column='quantity')
    minSecurityLevel = models.FloatField(blank=True, null=True, db_column='minSecurityLevel')

    def __unicode__(self):
        return '%s %s' % (self.towerType.name, self.resourceType.name)

    class Meta:
        db_table = 'invControlTowerResources'


class Location(models.Model):
    """Core model for SDD mapDenormalize table that generic locations map to."""
    itemid = models.IntegerField(primary_key=True, db_column='itemID')
    typeid = models.ForeignKey(Type, null=True, blank=True, related_name='mapentries',
            db_column='typeID')
    system = models.ForeignKey(SystemData, null=True, blank=True, related_name='mapentries',
            db_column='solarSystemID')
    constellation = models.ForeignKey(Constellation, null=True, blank=True, 
            related_name='mapentries', db_column='constellationID')
    region = models.ForeignKey(Region, null=True, blank=True, related_name='mapentries', 
            db_column='regionID')
    orbitparent = models.ForeignKey('Location', null=True, blank=True, 
            related_name='satellites', db_column='orbitID')
    name = models.CharField(max_length=100, null=True, blank=True, db_column='itemName')
    x = models.FloatField(null=True, blank=True, db_column='x')
    y = models.FloatField(null=True, blank=True, db_column='y')
    z = models.FloatField(null=True, blank=True, db_column='z')
    security = models.FloatField(null=True, blank=True, db_column='security')

    class Meta:
        db_table='mapDenormalize'


class LocationWormholeClass(models.Model):
    """Core model for SDD mapLocationWormholeClasses used to generate system tables."""
    location = models.ForeignKey(Location, primary_key=True, related_name="whclass",
            db_column='locationID')
    sysclass = models.IntegerField(null=True, blank=True, db_column='wormholeClassID')

    class Meta:
        db_table='mapLocationWormholeClasses'


class SystemJump(models.Model):
    """Core model for SDD mapSolarSystemJumps used in A* calcs."""
    fromregion = models.IntegerField(db_column="fromRegionID")
    fromconstellation = models.IntegerField(db_column="fromConstellationID")
    fromsystem = models.IntegerField(db_column="fromSolarSystemID", primary_key=True)
    tosystem = models.IntegerField(db_column="toSolarSystemID", primary_key=True)
    toconstellation = models.IntegerField(db_column="toConstellationID")
    toregion = models.IntegerField(db_column="toRegionID")

    class Meta:
        db_table='mapSolarSystemJumps'
