# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'APIKey'
        db.create_table('API_apikey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyid', self.gf('django.db.models.fields.IntegerField')()),
            ('vcode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lastvalidated', self.gf('django.db.models.fields.DateTimeField')()),
            ('proxykey', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('API', ['APIKey'])

        # Adding model 'CorpAPIKey'
        db.create_table('API_corpapikey', (
            ('apikey_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['API.APIKey'], unique=True, primary_key=True)),
            ('corp', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_keys', to=orm['core.Corporation'])),
        ))
        db.send_create_signal('API', ['CorpAPIKey'])

        # Adding model 'MemberAPIKey'
        db.create_table('API_memberapikey', (
            ('apikey_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['API.APIKey'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_keys', to=orm['auth.User'])),
        ))
        db.send_create_signal('API', ['MemberAPIKey'])

        # Adding model 'APICharacter'
        db.create_table('API_apicharacter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('apikey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='characters', to=orm['API.APIKey'])),
            ('charid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('corp', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('alliance', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastshipname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastshiptype', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('API', ['APICharacter'])

        # Adding model 'APIShipLog'
        db.create_table('API_apishiplog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shiplogs', to=orm['API.APICharacter'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('shiptype', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('shipname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('API', ['APIShipLog'])

        # Adding model 'APICachedDocument'
        db.create_table('API_apicacheddocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('params', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('xml', self.gf('django.db.models.fields.TextField')()),
            ('cacheduntil', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('API', ['APICachedDocument'])


    def backwards(self, orm):
        # Deleting model 'APIKey'
        db.delete_table('API_apikey')

        # Deleting model 'CorpAPIKey'
        db.delete_table('API_corpapikey')

        # Deleting model 'MemberAPIKey'
        db.delete_table('API_memberapikey')

        # Deleting model 'APICharacter'
        db.delete_table('API_apicharacter')

        # Deleting model 'APIShipLog'
        db.delete_table('API_apishiplog')

        # Deleting model 'APICachedDocument'
        db.delete_table('API_apicacheddocument')


    models = {
        'API.apicacheddocument': {
            'Meta': {'object_name': 'APICachedDocument'},
            'cacheduntil': ('django.db.models.fields.DateTimeField', [], {}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'params': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'xml': ('django.db.models.fields.TextField', [], {})
        },
        'API.apicharacter': {
            'Meta': {'object_name': 'APICharacter'},
            'alliance': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'apikey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'characters'", 'to': "orm['API.APIKey']"}),
            'charid': ('django.db.models.fields.BigIntegerField', [], {}),
            'corp': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastshipname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lastshiptype': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'API.apikey': {
            'Meta': {'object_name': 'APIKey'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyid': ('django.db.models.fields.IntegerField', [], {}),
            'lastvalidated': ('django.db.models.fields.DateTimeField', [], {}),
            'proxykey': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vcode': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'API.apishiplog': {
            'Meta': {'object_name': 'APIShipLog'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shiplogs'", 'to': "orm['API.APICharacter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shipname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shiptype': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'API.corpapikey': {
            'Meta': {'object_name': 'CorpAPIKey', '_ormbases': ['API.APIKey']},
            'apikey_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['API.APIKey']", 'unique': 'True', 'primary_key': 'True'}),
            'corp': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_keys'", 'to': "orm['core.Corporation']"})
        },
        'API.memberapikey': {
            'Meta': {'object_name': 'MemberAPIKey', '_ormbases': ['API.APIKey']},
            'apikey_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['API.APIKey']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_keys'", 'to': "orm['auth.User']"})
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
        'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': "orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['API']