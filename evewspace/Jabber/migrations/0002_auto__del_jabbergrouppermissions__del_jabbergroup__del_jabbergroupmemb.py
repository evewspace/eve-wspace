# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'JabberGroupPermissions'
        db.delete_table('Jabber_jabbergrouppermissions')

        # Deleting model 'JabberGroup'
        db.delete_table('Jabber_jabbergroup')

        # Deleting model 'JabberGroupMember'
        db.delete_table('Jabber_jabbergroupmember')

        # Adding model 'JabberSubscription'
        db.create_table('Jabber_jabbersubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jabber_subs', to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jabber_subs', to=orm['Alerts.SubscriptionGroup'])),
        ))
        db.send_create_signal('Jabber', ['JabberSubscription'])

        # Adding model 'JabberAccount'
        db.create_table('Jabber_jabberaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jabber_accounts', to=orm['auth.User'])),
            ('jid', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('Jabber', ['JabberAccount'])


    def backwards(self, orm):
        # Adding model 'JabberGroupPermissions'
        db.create_table('Jabber_jabbergrouppermissions', (
            ('jabbergroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='group_permissions', to=orm['Jabber.JabberGroup'])),
            ('canjoin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('usergroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jabber_groups', to=orm['auth.Group'])),
            ('canbroadcast', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('Jabber', ['JabberGroupPermissions'])

        # Adding model 'JabberGroup'
        db.create_table('Jabber_jabbergroup', (
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('Jabber', ['JabberGroup'])

        # Adding model 'JabberGroupMember'
        db.create_table('Jabber_jabbergroupmember', (
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='members', to=orm['Jabber.JabberGroup'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='jabber_groups', to=orm['auth.User'])),
        ))
        db.send_create_signal('Jabber', ['JabberGroupMember'])

        # Deleting model 'JabberSubscription'
        db.delete_table('Jabber_jabbersubscription')

        # Deleting model 'JabberAccount'
        db.delete_table('Jabber_jabberaccount')


    models = {
        'Alerts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Alerts.SubscriptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alert_groups'", 'to': "orm['auth.User']"})
        },
        'Alerts.subscriptiongroup': {
            'Meta': {'object_name': 'SubscriptionGroup'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['Alerts.Subscription']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Jabber.jabberaccount': {
            'Meta': {'object_name': 'JabberAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jabber_accounts'", 'to': "orm['auth.User']"})
        },
        'Jabber.jabbersubscription': {
            'Meta': {'object_name': 'JabberSubscription'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jabber_subs'", 'to': "orm['Alerts.SubscriptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jabber_subs'", 'to': "orm['auth.User']"})
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
        }
    }

    complete_apps = ['Jabber']