# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Action', fields ['name']
        db.delete_unique(u'Recruitment_action', ['name'])

        # Deleting model 'VoteAction'
        db.delete_table(u'Recruitment_voteaction')

        # Removing M2M table for field votes_for on 'VoteAction'
        db.delete_table(db.shorten_name(u'Recruitment_voteaction_votes_for'))

        # Removing M2M table for field votes_against on 'VoteAction'
        db.delete_table(db.shorten_name(u'Recruitment_voteaction_votes_against'))

        # Adding model 'VoteActionLog'
        db.create_table(u'Recruitment_voteactionlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vote_info', to=orm['Recruitment.ActionEntry'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ro_votes_for', to=orm['account.EWSUser'])),
            ('result', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Recruitment', ['VoteActionLog'])

        # Adding unique constraint on 'VoteActionLog', fields ['action_entry', 'voter']
        db.create_unique(u'Recruitment_voteactionlog', ['action_entry_id', 'voter_id'])


        # Changing field 'AppComment.author'
        db.alter_column(u'Recruitment_appcomment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'Interview.interviewer'
        db.alter_column(u'Recruitment_interview', 'interviewer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'CountersignAction.approver1'
        db.alter_column(u'Recruitment_countersignaction', 'approver1_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))

        # Changing field 'CountersignAction.approver2'
        db.alter_column(u'Recruitment_countersignaction', 'approver2_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))
        # Deleting field 'Action.descripiton'
        db.delete_column(u'Recruitment_action', 'descripiton')

        # Adding field 'Action.description'
        db.add_column(u'Recruitment_action', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Action.visible'
        db.add_column(u'Recruitment_action', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # Changing field 'Action.name'
        db.alter_column(u'Recruitment_action', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Application.applicant'
        db.alter_column(u'Recruitment_application', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'Application.closed_by'
        db.alter_column(u'Recruitment_application', 'closed_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))

        # Changing field 'AppVote.vote'
        db.alter_column(u'Recruitment_appvote', 'vote_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser']))

        # Changing field 'ApprovalAction.approver'
        db.alter_column(u'Recruitment_approvalaction', 'approver_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))
        # Deleting field 'AppType.deleted'
        db.delete_column(u'Recruitment_apptype', 'deleted')

        # Adding field 'AppType.required_votes'
        db.add_column(u'Recruitment_apptype', 'required_votes',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'AppType.visible'
        db.add_column(u'Recruitment_apptype', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'AppType.timestamp'
        db.add_column(u'Recruitment_apptype', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2015, 4, 27, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'AppStage.visible'
        db.add_column(u'Recruitment_appstage', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'AppQuestion.visible'
        db.add_column(u'Recruitment_appquestion', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'VoteActionLog', fields ['action_entry', 'voter']
        db.delete_unique(u'Recruitment_voteactionlog', ['action_entry_id', 'voter_id'])

        # Adding model 'VoteAction'
        db.create_table(u'Recruitment_voteaction', (
            ('action_entry', self.gf('django.db.models.fields.related.OneToOneField')(related_name='vote_info', unique=True, primary_key=True, to=orm['Recruitment.ActionEntry'])),
        ))
        db.send_create_signal(u'Recruitment', ['VoteAction'])

        # Adding M2M table for field votes_for on 'VoteAction'
        m2m_table_name = db.shorten_name(u'Recruitment_voteaction_votes_for')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voteaction', models.ForeignKey(orm[u'Recruitment.voteaction'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['voteaction_id', 'user_id'])

        # Adding M2M table for field votes_against on 'VoteAction'
        m2m_table_name = db.shorten_name(u'Recruitment_voteaction_votes_against')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('voteaction', models.ForeignKey(orm[u'Recruitment.voteaction'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['voteaction_id', 'user_id'])

        # Deleting model 'VoteActionLog'
        db.delete_table(u'Recruitment_voteactionlog')


        # Changing field 'AppComment.author'
        db.alter_column(u'Recruitment_appcomment', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Interview.interviewer'
        db.alter_column(u'Recruitment_interview', 'interviewer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'CountersignAction.approver1'
        db.alter_column(u'Recruitment_countersignaction', 'approver1_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'CountersignAction.approver2'
        db.alter_column(u'Recruitment_countersignaction', 'approver2_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
        # Adding field 'Action.descripiton'
        db.add_column(u'Recruitment_action', 'descripiton',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Action.description'
        db.delete_column(u'Recruitment_action', 'description')

        # Deleting field 'Action.visible'
        db.delete_column(u'Recruitment_action', 'visible')


        # Changing field 'Action.name'
        db.alter_column(u'Recruitment_action', 'name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))
        # Adding unique constraint on 'Action', fields ['name']
        db.create_unique(u'Recruitment_action', ['name'])


        # Changing field 'Application.applicant'
        db.alter_column(u'Recruitment_application', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Application.closed_by'
        db.alter_column(u'Recruitment_application', 'closed_by_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'AppVote.vote'
        db.alter_column(u'Recruitment_appvote', 'vote_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ApprovalAction.approver'
        db.alter_column(u'Recruitment_approvalaction', 'approver_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
        # Adding field 'AppType.deleted'
        db.add_column(u'Recruitment_apptype', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'AppType.required_votes'
        db.delete_column(u'Recruitment_apptype', 'required_votes')

        # Deleting field 'AppType.visible'
        db.delete_column(u'Recruitment_apptype', 'visible')

        # Deleting field 'AppType.timestamp'
        db.delete_column(u'Recruitment_apptype', 'timestamp')

        # Deleting field 'AppStage.visible'
        db.delete_column(u'Recruitment_appstage', 'visible')

        # Deleting field 'AppQuestion.visible'
        db.delete_column(u'Recruitment_appquestion', 'visible')


    models = {
        u'Map.map': {
            'Meta': {'object_name': 'Map'},
            'explicitperms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root'", 'to': u"orm['Map.System']"}),
            'truncate_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
        u'Recruitment.action': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Action'},
            'action_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required_votes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'Recruitment.actionentry': {
            'Meta': {'unique_together': "(['action', 'application'],)", 'object_name': 'ActionEntry'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Recruitment.Action']"}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Recruitment.Application']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Recruitment.appcomment': {
            'Meta': {'object_name': 'AppComment'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': u"orm['Recruitment.Application']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_comments'", 'to': u"orm['account.EWSUser']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'Recruitment.application': {
            'Meta': {'object_name': 'Application'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'to': u"orm['Recruitment.AppType']"}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'to': u"orm['account.EWSUser']"}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications_closed'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'closetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 4, 27, 0, 0)'}),
            'disposition': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'Recruitment.appquestion': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppQuestion'},
            'app_stage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['Recruitment.AppStage']"}),
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['Recruitment.AppType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'Recruitment.appquestionchoice': {
            'Meta': {'object_name': 'AppQuestionChoice'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['Recruitment.AppQuestion']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'Recruitment.appresponse': {
            'Meta': {'object_name': 'AppResponse'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['Recruitment.Application']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': u"orm['Recruitment.AppQuestion']"}),
            'response': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Recruitment.approvalaction': {
            'Meta': {'object_name': 'ApprovalAction', '_ormbases': [u'Recruitment.ActionEntry']},
            'action_entry': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'approval_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['Recruitment.ActionEntry']"}),
            'approval_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approval_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_approvals'", 'null': 'True', 'to': u"orm['account.EWSUser']"})
        },
        u'Recruitment.appstage': {
            'Meta': {'ordering': "['order']", 'object_name': 'AppStage'},
            'app_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stages'", 'to': u"orm['Recruitment.AppType']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'Recruitment.apptype': {
            'Meta': {'object_name': 'AppType'},
            'accept_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': u"orm['auth.Group']"}),
            'accept_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'accept_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'defer_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'defer_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'disable_user_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'purge_api_on_failure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reject_mail': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'reject_subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'require_account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'required_votes': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'use_standings': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'applications'", 'null': 'True', 'to': u"orm['core.Corporation']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'Recruitment.appvote': {
            'Meta': {'object_name': 'AppVote'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': u"orm['Recruitment.Application']"}),
            'disposition': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appvotes'", 'to': u"orm['account.EWSUser']"})
        },
        u'Recruitment.countersignaction': {
            'Meta': {'object_name': 'CountersignAction', '_ormbases': [u'Recruitment.ActionEntry']},
            'action_entry': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'countersign_info'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['Recruitment.ActionEntry']"}),
            'approver1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counter_approve1'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'approver1_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approver1_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'approver2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'counter_approve2'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'approver2_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approver2_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'Recruitment.interview': {
            'Meta': {'object_name': 'Interview'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': u"orm['Recruitment.Application']"}),
            'chatlog': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interviews'", 'to': u"orm['account.EWSUser']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'Recruitment.standigsrequirement': {
            'Meta': {'object_name': 'StandigsRequirement'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'entitytype': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'standing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'Recruitment.voteactionlog': {
            'Meta': {'unique_together': "(['action_entry', 'voter'],)", 'object_name': 'VoteActionLog'},
            'action_entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vote_info'", 'to': u"orm['Recruitment.ActionEntry']"}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ro_votes_for'", 'to': u"orm['account.EWSUser']"})
        },
        u'account.ewsuser': {
            'Meta': {'object_name': 'EWSUser'},
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
        }
    }

    complete_apps = ['Recruitment']