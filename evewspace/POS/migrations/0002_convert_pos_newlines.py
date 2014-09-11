# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        for pos in orm.POS.objects.all():
            save = False
            if pos.fitting:
                pos.fitting = pos.fitting.replace('<br />', '\n')
                save = True
            if save:
                pos.save()
    def backwards(self, orm):
        "Write your backwards methods here."
        for pos in orm.POS.objects.all():
            save = False
            if pos.fitting:
                pos.fitting = pos.fitting.replace('\n', '<br />')
                save = True
            if save:
                pos.save()

    models = {
        u'API.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'access_mask': ('django.db.models.fields.IntegerField', [], {}),
            'keyid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'lastvalidated': ('django.db.models.fields.DateTimeField', [], {}),
            'proxykey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validation_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'API.corpapikey': {
            'Meta': {'object_name': 'CorpAPIKey', '_ormbases': [u'API.APIKey']},
            u'apikey_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['API.APIKey']", 'unique': 'True', 'primary_key': 'True'}),
            'character_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_keys'", 'to': u"orm['core.Corporation']"})
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
        u'POS.corppos': {
            'Meta': {'ordering': "['system__name', 'planet', 'moon']", 'object_name': 'CorpPOS', '_ormbases': [u'POS.POS']},
            'apiitemid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poses'", 'null': 'True', 'to': u"orm['API.CorpAPIKey']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poses'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'pos_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['POS.POS']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'POS.pos': {
            'Meta': {'ordering': "['system__name', 'planet', 'moon']", 'object_name': 'POS'},
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poses'", 'to': u"orm['core.Corporation']"}),
            'ewar': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fitting': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'guns': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hardener': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moon': ('django.db.models.fields.IntegerField', [], {}),
            'planet': ('django.db.models.fields.IntegerField', [], {}),
            'posname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rftime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poses'", 'to': u"orm['Map.System']"}),
            'towertype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inspace'", 'to': u"orm['core.Type']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'warpin_notice': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'POS.posapplication': {
            'Meta': {'object_name': 'POSApplication'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posapps'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalfit': ('django.db.models.fields.TextField', [], {}),
            'posrecord': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'application'", 'null': 'True', 'to': u"orm['POS.CorpPOS']"}),
            'residents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'siegefit': ('django.db.models.fields.TextField', [], {}),
            'towertype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posapps'", 'null': 'True', 'to': u"orm['core.Type']"})
        },
        u'POS.posvote': {
            'Meta': {'object_name': 'POSVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['POS.POSApplication']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vote': ('django.db.models.fields.IntegerField', [], {}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posvotes'", 'to': u"orm['auth.User']"})
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': u"orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.marketgroup': {
            'Meta': {'object_name': 'MarketGroup', 'db_table': "'invMarketGroups'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hasTypes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'marketGroupID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'marketGroupName'", 'blank': 'True'}),
            'parentgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childgroups'", 'null': 'True', 'db_column': "'parentGroupID'", 'to': u"orm['core.MarketGroup']"})
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
        u'core.type': {
            'Meta': {'object_name': 'Type', 'db_table': "'invTypes'", 'managed': 'False'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'typeID'"}),
            'marketgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'types'", 'null': 'True', 'db_column': "'marketGroupID'", 'to': u"orm['core.MarketGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'typeName'"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['POS']
    symmetrical = True
