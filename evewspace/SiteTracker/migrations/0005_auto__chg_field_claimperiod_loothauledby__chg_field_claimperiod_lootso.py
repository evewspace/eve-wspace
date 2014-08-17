# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ClaimPeriod.loothauledby'
        db.alter_column(u'SiteTracker_claimperiod', 'loothauledby_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))

        # Changing field 'ClaimPeriod.lootsoldby'
        db.alter_column(u'SiteTracker_claimperiod', 'lootsoldby_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))
        # Adding field 'UserSite.tenant'
        db.add_column(u'SiteTracker_usersite', 'tenant',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='site_records', to=orm['core.Tenant']),
                      keep_default=False)


        # Changing field 'UserSite.user'
        db.alter_column(u'SiteTracker_usersite', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'PayoutEntry.user'
        db.alter_column(u'SiteTracker_payoutentry', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'Claim.user'
        db.alter_column(u'SiteTracker_claim', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))
        # Adding field 'Fleet.tenant'
        db.add_column(u'SiteTracker_fleet', 'tenant',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='stfleets', to=orm['core.Tenant']),
                      keep_default=False)


        # Changing field 'Fleet.current_boss'
        db.alter_column(u'SiteTracker_fleet', 'current_boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'Fleet.initial_boss'
        db.alter_column(u'SiteTracker_fleet', 'initial_boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'PayoutReport.createdby'
        db.alter_column(u'SiteTracker_payoutreport', 'createdby_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'UserLog.user'
        db.alter_column(u'SiteTracker_userlog', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'SiteRecord.boss'
        db.alter_column(u'SiteTracker_siterecord', 'boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

    def backwards(self, orm):

        # Changing field 'ClaimPeriod.loothauledby'
        db.alter_column(u'SiteTracker_claimperiod', 'loothauledby_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'ClaimPeriod.lootsoldby'
        db.alter_column(u'SiteTracker_claimperiod', 'lootsoldby_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
        # Deleting field 'UserSite.tenant'
        db.delete_column(u'SiteTracker_usersite', 'tenant_id')


        # Changing field 'UserSite.user'
        db.alter_column(u'SiteTracker_usersite', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'PayoutEntry.user'
        db.alter_column(u'SiteTracker_payoutentry', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Claim.user'
        db.alter_column(u'SiteTracker_claim', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        # Deleting field 'Fleet.tenant'
        db.delete_column(u'SiteTracker_fleet', 'tenant_id')


        # Changing field 'Fleet.current_boss'
        db.alter_column(u'SiteTracker_fleet', 'current_boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Fleet.initial_boss'
        db.alter_column(u'SiteTracker_fleet', 'initial_boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'PayoutReport.createdby'
        db.alter_column(u'SiteTracker_payoutreport', 'createdby_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'UserLog.user'
        db.alter_column(u'SiteTracker_userlog', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'SiteRecord.boss'
        db.alter_column(u'SiteTracker_siterecord', 'boss_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    models = {
        u'Map.map': {
            'Meta': {'object_name': 'Map'},
            'explicitperms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root'", 'to': u"orm['Map.System']"}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maps'", 'to': u"orm['core.Tenant']"})
        },
        u'Map.system': {
            'Meta': {'object_name': 'System', '_ormbases': [u'core.SystemData']},
            'first_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastscanned': ('django.db.models.fields.DateTimeField', [], {}),
            'npckills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'occupied': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {}),
            u'systemdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.SystemData']", 'unique': 'True', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'SiteTracker.claim': {
            'Meta': {'object_name': 'Claim'},
            'bonus': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': u"orm['SiteTracker.ClaimPeriod']"}),
            'shareclaimed': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': u"orm['account.EWSUser']"})
        },
        u'SiteTracker.claimperiod': {
            'Meta': {'object_name': 'ClaimPeriod'},
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loothauledby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loothauled'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'lootsoldby': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lootsold'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'SiteTracker.fleet': {
            'Meta': {'object_name': 'Fleet'},
            'current_boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'currently_bossing'", 'to': u"orm['account.EWSUser']"}),
            'ended': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bossfleets'", 'to': u"orm['account.EWSUser']"}),
            'roles_needed': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fleets_need'", 'symmetrical': 'False', 'to': u"orm['SiteTracker.SiteRole']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stfleets'", 'to': u"orm['Map.System']"}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stfleets'", 'to': u"orm['core.Tenant']"})
        },
        u'SiteTracker.payoutentry': {
            'Meta': {'object_name': 'PayoutEntry'},
            'claim': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payout'", 'to': u"orm['SiteTracker.Claim']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iskshare': ('django.db.models.fields.BigIntegerField', [], {}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['SiteTracker.PayoutReport']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payouts'", 'to': u"orm['account.EWSUser']"})
        },
        u'SiteTracker.payoutreport': {
            'Meta': {'object_name': 'PayoutReport'},
            'createdby': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payoutreports'", 'to': u"orm['account.EWSUser']"}),
            'datepaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'grossprofit': ('django.db.models.fields.BigIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reports'", 'to': u"orm['SiteTracker.ClaimPeriod']"})
        },
        u'SiteTracker.siterecord': {
            'Meta': {'object_name': 'SiteRecord'},
            'boss': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitescredited'", 'to': u"orm['account.EWSUser']"}),
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': u"orm['SiteTracker.Fleet']"}),
            'fleetsize': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_points': ('django.db.models.fields.IntegerField', [], {}),
            'site_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitesrun'", 'to': u"orm['SiteTracker.SiteType']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitescompleted'", 'to': u"orm['Map.System']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'weighted_points': ('django.db.models.fields.FloatField', [], {})
        },
        u'SiteTracker.siterole': {
            'Meta': {'object_name': 'SiteRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'SiteTracker.sitetype': {
            'Meta': {'object_name': 'SiteType'},
            'defunct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'shortname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'})
        },
        u'SiteTracker.siteweight': {
            'Meta': {'object_name': 'SiteWeight'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'raw_points': ('django.db.models.fields.IntegerField', [], {}),
            'site_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weights'", 'to': u"orm['SiteTracker.SiteType']"}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {})
        },
        u'SiteTracker.systemweight': {
            'Meta': {'object_name': 'SystemWeight'},
            'system': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'st_weight'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['Map.System']"}),
            'weight': ('django.db.models.fields.FloatField', [], {})
        },
        u'SiteTracker.userlog': {
            'Meta': {'object_name': 'UserLog'},
            'fleet': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': u"orm['SiteTracker.Fleet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jointime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'leavetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sitetrackerlogs'", 'to': u"orm['account.EWSUser']"})
        },
        u'SiteTracker.usersite': {
            'Meta': {'object_name': 'UserSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': u"orm['SiteTracker.SiteRecord']"}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'site_records'", 'to': u"orm['core.Tenant']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': u"orm['account.EWSUser']"})
        },
        u'account.ewsuser': {
            'Meta': {'object_name': 'EWSUser'},
            'current_tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'active_users'", 'null': 'True', 'to': u"orm['core.Tenant']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'defaultmap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'defaultusers'", 'null': 'True', 'to': u"orm['Map.Map']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.constellation': {
            'Meta': {'object_name': 'Constellation', 'db_table': "'mapConstellations'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'constellationID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'constellationName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'constellations'", 'db_column': "'regionID'", 'to': u"orm['core.Region']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'mapRegions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'regionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'regionName'"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.systemdata': {
            'Meta': {'object_name': 'SystemData', 'db_table': "'mapSolarSystems'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'constellationID'", 'to': u"orm['core.Constellation']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'solarSystemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'solarSystemName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'regionID'", 'to': u"orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.tenant': {
            'Meta': {'object_name': 'Tenant'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'admin_notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['SiteTracker']