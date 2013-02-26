# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TeamspeakServer'
        db.create_table('Teamspeak_teamspeakserver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('queryuser', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('querypass', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('queryport', self.gf('django.db.models.fields.IntegerField')()),
            ('voiceport', self.gf('django.db.models.fields.IntegerField')()),
            ('enforcegroups', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enforeceusers', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Teamspeak', ['TeamspeakServer'])

        # Adding model 'GroupMap'
        db.create_table('Teamspeak_groupmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tsserver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupmaps', to=orm['Teamspeak.TeamspeakServer'])),
            ('usergroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='teamspeakgroups', to=orm['auth.Group'])),
            ('tsgroup', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('Teamspeak', ['GroupMap'])


    def backwards(self, orm):
        # Deleting model 'TeamspeakServer'
        db.delete_table('Teamspeak_teamspeakserver')

        # Deleting model 'GroupMap'
        db.delete_table('Teamspeak_groupmap')


    models = {
        'Teamspeak.groupmap': {
            'Meta': {'object_name': 'GroupMap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tsgroup': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tsserver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupmaps'", 'to': "orm['Teamspeak.TeamspeakServer']"}),
            'usergroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'teamspeakgroups'", 'to': "orm['auth.Group']"})
        },
        'Teamspeak.teamspeakserver': {
            'Meta': {'object_name': 'TeamspeakServer'},
            'enforcegroups': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enforeceusers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'querypass': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'queryport': ('django.db.models.fields.IntegerField', [], {}),
            'queryuser': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'voiceport': ('django.db.models.fields.IntegerField', [], {})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Teamspeak']