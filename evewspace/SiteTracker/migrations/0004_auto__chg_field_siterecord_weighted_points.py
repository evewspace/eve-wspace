# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SiteRecord.weighted_points'
        db.alter_column('SiteTracker_siterecord', 'weighted_points', self.gf('django.db.models.fields.FloatField')())

    def backwards(self, orm):

        # Changing field 'SiteRecord.weighted_points'
        db.alter_column('SiteTracker_siterecord', 'weighted_points', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'Map.system': {
            'Meta': {'object_name': 'System', '_ormbases': ['core.SystemData']},
            'first_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastscanned': ('django.db.models.fields.DateTimeField', [], {}),
            'npckills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'occupied': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {}),
            'systemdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SystemData']", 'unique': 'True', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'SiteTracker.claim': {
            'Meta': {'object_name': 'Claim'},
            'bonus': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': "orm['SiteTracker.ClaimPeriod']"}),
            'shareclaimed': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': "orm['auth.User']"})
        },
        'SiteTracker.claimperiod': {
            'Meta': {'object_name': 'ClaimPeriod'},
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loothauledby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loothauled'", 'null': 'True', 'to': "orm['auth.User']"}),
            'lootsoldby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lootsold'", 'null': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {})
        },
        'SiteTracker.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'current_boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currently_bossing'", 'to': "orm['auth.User']"}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bossfleets'", 'to': "orm['auth.User']"}),
            'roles_needed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fleets_need'", 'symmetrical': 'False', 'to': "orm['SiteTracker.SiteRole']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stfleets'", 'to': "orm['Map.System']"})
        },
        'SiteTracker.payoutentry': {
            'Meta': {'object_name': 'PayoutEntry'},
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payout'", 'to': "orm['SiteTracker.Claim']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iskshare': ('django.db.models.fields.BigIntegerField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['SiteTracker.PayoutReport']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payouts'", 'to': "orm['auth.User']"})
        },
        'SiteTracker.payoutreport': {
            'Meta': {'object_name': 'PayoutReport'},
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payoutreports'", 'to': "orm['auth.User']"}),
            'datepaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'grossprofit': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': "orm['SiteTracker.ClaimPeriod']"})
        },
        'SiteTracker.siterecord': {
            'Meta': {'object_name': 'SiteRecord'},
            'boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitescredited'", 'to': "orm['auth.User']"}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': "orm['SiteTracker.Fleet']"}),
            'fleetsize': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_points': ('django.db.models.fields.IntegerField', [], {}),
            'site_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitesrun'", 'to': "orm['SiteTracker.SiteType']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitescompleted'", 'to': "orm['Map.System']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'weighted_points': ('django.db.models.fields.FloatField', [], {})
        },
        'SiteTracker.siterole': {
            'Meta': {'object_name': 'SiteRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'SiteTracker.sitetype': {
            'Meta': {'object_name': 'SiteType'},
            'defunct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        'SiteTracker.siteweight': {
            'Meta': {'object_name': 'SiteWeight'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_points': ('django.db.models.fields.IntegerField', [], {}),
            'site_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weights'", 'to': "orm['SiteTracker.SiteType']"}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {})
        },
        'SiteTracker.systemweight': {
            'Meta': {'object_name': 'SystemWeight'},
            'system': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'st_weight'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['Map.System']"}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        'SiteTracker.userlog': {
            'Meta': {'object_name': 'UserLog'},
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': "orm['SiteTracker.Fleet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jointime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'leavetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitetrackerlogs'", 'to': "orm['auth.User']"})
        },
        'SiteTracker.usersite': {
            'Meta': {'object_name': 'UserSite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': "orm['SiteTracker.SiteRecord']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': "orm['auth.User']"})
        },
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
        'core.constellation': {
            'Meta': {'object_name': 'Constellation', 'db_table': "'mapConstellations'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'constellationID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'constellationName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'constellations'", 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'mapRegions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'regionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'regionName'"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
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
        }
    }

    complete_apps = ['SiteTracker']