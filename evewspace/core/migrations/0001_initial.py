# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewsFeed'
        db.create_table('core_newsfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feeds', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['NewsFeed'])

        # Adding model 'Alliance'
        db.create_table('core_alliance', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('executor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['core.Corporation'])),
        ))
        db.send_create_signal('core', ['Alliance'])

        # Adding model 'Corporation'
        db.create_table('core_corporation', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('alliance', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='member_corps', null=True, to=orm['core.Alliance'])),
            ('member_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['Corporation'])

        # Adding model 'ConfigEntry'
        db.create_table('core_configentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='settings', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('core', ['ConfigEntry'])


    def backwards(self, orm):
        # Deleting model 'NewsFeed'
        db.delete_table('core_newsfeed')

        # Deleting model 'Alliance'
        db.delete_table('core_alliance')

        # Deleting model 'Corporation'
        db.delete_table('core_corporation')

        # Deleting model 'ConfigEntry'
        db.delete_table('core_configentry')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.configentry': {
            'Meta': {'object_name': 'ConfigEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'settings'", 'null': 'True', 'to': "orm['auth.User']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'core.constellation': {
            'Meta': {'object_name': 'Constellation', 'db_table': "'mapConstellations'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'constellationID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'constellationName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'constellations'", 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': "orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.faction': {
            'Meta': {'object_name': 'Faction', 'db_table': "u'chrFactions'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'blank': 'True'}),
            'iconid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'iconID'", 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'factionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'factionName'", 'blank': 'True'})
        },
        'core.location': {
            'Meta': {'object_name': 'Location', 'db_table': "'mapDenormalize'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'constellationID'", 'to': "orm['core.Constellation']"}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'itemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'itemName'", 'blank': 'True'}),
            'orbitparent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'satellites'", 'null': 'True', 'db_column': "'orbitID'", 'to': "orm['core.Location']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'security'", 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'solarSystemID'", 'to': "orm['core.SystemData']"}),
            'typeid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'typeID'", 'to': "orm['core.Type']"}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'x'", 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'y'", 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'z'", 'blank': 'True'})
        },
        'core.locationwormholeclass': {
            'Meta': {'object_name': 'LocationWormholeClass', 'db_table': "'mapLocationWormholeClasses'", 'managed': 'False'},
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whclass'", 'primary_key': 'True', 'db_column': "'locationID'", 'to': "orm['core.Location']"}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'wormholeClassID'", 'blank': 'True'})
        },
        'core.marketgroup': {
            'Meta': {'object_name': 'MarketGroup', 'db_table': "'invMarketGroups'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hasTypes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'marketGroupID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'marketGroupName'", 'blank': 'True'}),
            'parentgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childgroups'", 'null': 'True', 'db_column': "'parentGroupID'", 'to': "orm['core.MarketGroup']"})
        },
        'core.newsfeed': {
            'Meta': {'ordering': "['name']", 'object_name': 'NewsFeed'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'core.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'mapRegions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'regionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'regionName'"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.starbaseresource': {
            'Meta': {'object_name': 'StarbaseResource', 'db_table': "'invControlTowerResources'", 'managed': 'False'},
            'minSecurityLevel': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'minSecurityLevel'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'usedby'", 'null': 'True', 'db_column': "'purpose'", 'to': "orm['core.StarbaseResourcePurpose']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'quantity'", 'blank': 'True'}),
            'resourceType': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posfuel'", 'db_column': "'resourceTypeID'", 'to': "orm['core.Type']"}),
            'towerType': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posesfueled'", 'primary_key': 'True', 'db_column': "'controlTowerTypeID'", 'to': "orm['core.Type']"})
        },
        'core.starbaseresourcepurpose': {
            'Meta': {'object_name': 'StarbaseResourcePurpose', 'db_table': "'invControlTowerResourcePurposes'", 'managed': 'False'},
            'purpose': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'purposeText': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'core.systemdata': {
            'Meta': {'object_name': 'SystemData', 'db_table': "'mapSolarSystems'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'constellationID'", 'to': "orm['core.Constellation']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'solarSystemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'solarSystemName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.systemjump': {
            'Meta': {'object_name': 'SystemJump', 'db_table': "'mapSolarSystemJumps'", 'managed': 'False'},
            'fromconstellation': ('django.db.models.fields.IntegerField', [], {'db_column': "'fromConstellationID'"}),
            'fromregion': ('django.db.models.fields.IntegerField', [], {'db_column': "'fromRegionID'"}),
            'fromsystem': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'fromSolarSystemID'"}),
            'toconstellation': ('django.db.models.fields.IntegerField', [], {'db_column': "'toConstellationID'"}),
            'toregion': ('django.db.models.fields.IntegerField', [], {'db_column': "'toRegionID'"}),
            'tosystem': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'toSolarSystemID'"})
        },
        'core.type': {
            'Meta': {'object_name': 'Type', 'db_table': "'invTypes'", 'managed': 'False'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'typeID'"}),
            'marketgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'types'", 'null': 'True', 'db_column': "'marketGroupID'", 'to': "orm['core.MarketGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'typeName'"}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']