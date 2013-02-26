# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Interest'
        db.create_table('Recruitment_interest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('Recruitment', ['Interest'])

        # Adding model 'Action'
        db.create_table('Recruitment_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('Recruitment', ['Action'])

        # Adding model 'Application'
        db.create_table('Recruitment_application', (
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='application', unique=True, primary_key=True, to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('killboard', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('closetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('disposition', self.gf('django.db.models.fields.IntegerField')()),
            ('intelclear', self.gf('django.db.models.fields.DateTimeField')()),
            ('standingsclear', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Recruitment', ['Application'])

        # Adding M2M table for field interests on 'Application'
        db.create_table('Recruitment_application_interests', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('application', models.ForeignKey(orm['Recruitment.application'], null=False)),
            ('interest', models.ForeignKey(orm['Recruitment.interest'], null=False))
        ))
        db.create_unique('Recruitment_application_interests', ['application_id', 'interest_id'])

        # Adding model 'AppVote'
        db.create_table('Recruitment_appvote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['Recruitment.Application'])),
            ('vote', self.gf('django.db.models.fields.related.ForeignKey')(related_name='appvotes', to=orm['auth.User'])),
            ('disposition', self.gf('django.db.models.fields.IntegerField')()),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('Recruitment', ['AppVote'])

        # Adding model 'AppAction'
        db.create_table('Recruitment_appaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['Recruitment.Application'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['Recruitment.Action'])),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('Recruitment', ['AppAction'])

        # Adding model 'Interview'
        db.create_table('Recruitment_interview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interviews', to=orm['Recruitment.Application'])),
            ('interviewer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='interviews', to=orm['auth.User'])),
            ('chatlog', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('Recruitment', ['Interview'])

        # Adding model 'AppQuestion'
        db.create_table('Recruitment_appquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('Recruitment', ['AppQuestion'])

        # Adding model 'AppResponse'
        db.create_table('Recruitment_appresponse', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['Recruitment.Application'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['Recruitment.AppQuestion'])),
            ('response', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('Recruitment', ['AppResponse'])

        # Adding model 'StandigsRequirement'
        db.create_table('Recruitment_standigsrequirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('standing', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('entitytype', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Recruitment', ['StandigsRequirement'])


    def backwards(self, orm):
        # Deleting model 'Interest'
        db.delete_table('Recruitment_interest')

        # Deleting model 'Action'
        db.delete_table('Recruitment_action')

        # Deleting model 'Application'
        db.delete_table('Recruitment_application')

        # Removing M2M table for field interests on 'Application'
        db.delete_table('Recruitment_application_interests')

        # Deleting model 'AppVote'
        db.delete_table('Recruitment_appvote')

        # Deleting model 'AppAction'
        db.delete_table('Recruitment_appaction')

        # Deleting model 'Interview'
        db.delete_table('Recruitment_interview')

        # Deleting model 'AppQuestion'
        db.delete_table('Recruitment_appquestion')

        # Deleting model 'AppResponse'
        db.delete_table('Recruitment_appresponse')

        # Deleting model 'StandigsRequirement'
        db.delete_table('Recruitment_standigsrequirement')


    models = {
        'Recruitment.action': {
            'Meta': {'object_name': 'Action'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'Recruitment.appaction': {
            'Meta': {'object_name': 'AppAction'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['Recruitment.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['Recruitment.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'Recruitment.application': {
            'Meta': {'object_name': 'Application'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'application'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['auth.User']"}),
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            'intelclear': ('django.db.models.fields.DateTimeField', [], {}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Recruitment.Interest']", 'symmetrical': 'False'}),
            'killboard': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'standingsclear': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'Recruitment.appquestion': {
            'Meta': {'object_name': 'AppQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'Recruitment.appresponse': {
            'Meta': {'object_name': 'AppResponse'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['Recruitment.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['Recruitment.AppQuestion']"}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'Recruitment.appvote': {
            'Meta': {'object_name': 'AppVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['Recruitment.Application']"}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appvotes'", 'to': "orm['auth.User']"})
        },
        'Recruitment.interest': {
            'Meta': {'object_name': 'Interest'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'Recruitment.interview': {
            'Meta': {'object_name': 'Interview'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['Recruitment.Application']"}),
            'chatlog': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': "orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'Recruitment.standigsrequirement': {
            'Meta': {'object_name': 'StandigsRequirement'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'entitytype': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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

    complete_apps = ['Recruitment']