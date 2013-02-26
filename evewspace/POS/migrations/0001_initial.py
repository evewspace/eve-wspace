# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'POS'
        db.create_table('POS_pos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poses', to=orm['Map.System'])),
            ('planet', self.gf('django.db.models.fields.IntegerField')()),
            ('moon', self.gf('django.db.models.fields.IntegerField')()),
            ('towertype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inspace', to=orm['core.Type'])),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(related_name='poses', to=orm['core.Corporation'])),
            ('posname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('fitting', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('rftime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('guns', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ewar', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sma', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hardener', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('warpin_notice', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('POS', ['POS'])

        # Adding model 'CorpPOS'
        db.create_table('POS_corppos', (
            ('pos_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['POS.POS'], unique=True, primary_key=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='poses', null=True, to=orm['auth.User'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('apiitemid', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('apikey', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='poses', null=True, to=orm['API.CorpAPIKey'])),
        ))
        db.send_create_signal('POS', ['CorpPOS'])

        # Adding model 'POSApplication'
        db.create_table('POS_posapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posapps', null=True, to=orm['auth.User'])),
            ('towertype', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posapps', null=True, to=orm['core.Type'])),
            ('normalfit', self.gf('django.db.models.fields.TextField')()),
            ('siegefit', self.gf('django.db.models.fields.TextField')()),
            ('approved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('posrecord', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='application', null=True, to=orm['POS.CorpPOS'])),
        ))
        db.send_create_signal('POS', ['POSApplication'])

        # Adding M2M table for field residents on 'POSApplication'
        db.create_table('POS_posapplication_residents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('posapplication', models.ForeignKey(orm['POS.posapplication'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('POS_posapplication_residents', ['posapplication_id', 'user_id'])

        # Adding model 'POSVote'
        db.create_table('POS_posvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['POS.POSApplication'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posvotes', to=orm['auth.User'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('POS', ['POSVote'])


    def backwards(self, orm):
        # Deleting model 'POS'
        db.delete_table('POS_pos')

        # Deleting model 'CorpPOS'
        db.delete_table('POS_corppos')

        # Deleting model 'POSApplication'
        db.delete_table('POS_posapplication')

        # Removing M2M table for field residents on 'POSApplication'
        db.delete_table('POS_posapplication_residents')

        # Deleting model 'POSVote'
        db.delete_table('POS_posvote')


    models = {
        'API.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyid': ('django.db.models.fields.IntegerField', [], {}),
            'lastvalidated': ('django.db.models.fields.DateTimeField', [], {}),
            'proxykey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'API.corpapikey': {
            'Meta': {'object_name': 'CorpAPIKey', '_ormbases': ['API.APIKey']},
            'apikey_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['API.APIKey']", 'unique': 'True', 'primary_key': 'True'}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_keys'", 'to': "orm['core.Corporation']"})
        },
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
        'POS.corppos': {
            'Meta': {'ordering': "['system__name', 'planet', 'moon']", 'object_name': 'CorpPOS', '_ormbases': ['POS.POS']},
            'apiitemid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poses'", 'null': 'True', 'to': "orm['API.CorpAPIKey']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'poses'", 'null': 'True', 'to': "orm['auth.User']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pos_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['POS.POS']", 'unique': 'True', 'primary_key': 'True'})
        },
        'POS.pos': {
            'Meta': {'ordering': "['system__name', 'planet', 'moon']", 'object_name': 'POS'},
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poses'", 'to': "orm['core.Corporation']"}),
            'ewar': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fitting': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'guns': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hardener': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moon': ('django.db.models.fields.IntegerField', [], {}),
            'planet': ('django.db.models.fields.IntegerField', [], {}),
            'posname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rftime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poses'", 'to': "orm['Map.System']"}),
            'towertype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inspace'", 'to': "orm['core.Type']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {}),
            'warpin_notice': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'POS.posapplication': {
            'Meta': {'object_name': 'POSApplication'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posapps'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalfit': ('django.db.models.fields.TextField', [], {}),
            'posrecord': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'application'", 'null': 'True', 'to': "orm['POS.CorpPOS']"}),
            'residents': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'siegefit': ('django.db.models.fields.TextField', [], {}),
            'towertype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posapps'", 'null': 'True', 'to': "orm['core.Type']"})
        },
        'POS.posvote': {
            'Meta': {'object_name': 'POSVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['POS.POSApplication']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vote': ('django.db.models.fields.IntegerField', [], {}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posvotes'", 'to': "orm['auth.User']"})
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
        'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'core.marketgroup': {
            'Meta': {'object_name': 'MarketGroup', 'db_table': "'invMarketGroups'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hasTypes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'marketGroupID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'marketGroupName'", 'blank': 'True'}),
            'parentgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childgroups'", 'null': 'True', 'db_column': "'parentGroupID'", 'to': "orm['core.MarketGroup']"})
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

    complete_apps = ['POS']