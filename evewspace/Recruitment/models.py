#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django import forms
from core.models import Corporation, Alliance
from account.models import EWSUserCreationForm

from datetime import datetime
import pytz
# Create your models here.

User = settings.AUTH_USER_MODEL

class Action(models.Model):
    """
    Represents an action that can be taken on an application e.g Intel Ran
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    action_type = models.IntegerField(default=1, choices=((1, 'Approval'),
        (2, 'Countersign'), (3, 'Vote')))
    visible = models.BooleanField(default=True)
    required_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

class ActionEntry(models.Model):
    action = models.ForeignKey(Action)
    application = models.ForeignKey('Application')
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['action', 'application']


class ApprovalAction(ActionEntry):
    action_entry = models.OneToOneField(ActionEntry,
            related_name='approval_info', parent_link=True)
    approver = models.ForeignKey(User, related_name="ro_approvals", null=True)
    approval_comment = models.TextField(null=True, blank=True)
    approval_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.approver:
            self.completed = True
        else:
            self.completed = False
        super(ApprovalAction, self).save(*args, **kwargs)


class CountersignAction(ActionEntry):
    action_entry = models.OneToOneField(ActionEntry,
            related_name='countersign_info', parent_link=True)
    approver1 = models.ForeignKey(User, null=True,
            related_name="counter_approve1")
    approver2 = models.ForeignKey(User, null=True,
            related_name="counter_approve2")
    approver1_comment = models.TextField(null=True, blank=True)
    approver1_time = models.DateTimeField(null=True)
    approver2_comment = models.TextField(null=True, blank=True)
    approver2_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.approver1 and self.approver2:
            self.completed = True
        else:
            self.completed = False
        super(CountersignAction, self).save(*args, **kwargs)


class VoteActionLog(models.Model):
    action_entry = models.ForeignKey(ActionEntry, related_name='vote_info')
    voter = models.ForeignKey(User, related_name='ro_votes_for')
    result = models.IntegerField(null=True, choices=((0,'Against'), (1,'For')))
    comment = models.TextField(null=True, blank=True)
    
    class Meta:
        unique_together = ['action_entry', 'voter']


class AppComment(models.Model):
    application = models.ForeignKey('Application', related_name="ro_comments")
    author = models.ForeignKey(User, related_name="ro_comments")
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    """Represents a recruitment application."""
    applicant = models.ForeignKey(User, related_name="applications")
    app_type = models.ForeignKey('AppType', related_name="applications")
    timestamp = models.DateTimeField(auto_now=True)
    #closetime = None indicates that the application is still open
    closetime = models.DateTimeField(null=True)
    created = models.DateTimeField(default=datetime.now(pytz.utc))
    submitted = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(User, related_name="applications_closed",
            null=True)
    disposition = models.IntegerField(null=True, choices=((0,'Duplicate'),
        (1,'Accepted'), (2,'Rejected'), (3, 'Deferred')))
    status_text = models.TextField(null=True)

    class Meta:
        permissions = (('can_recruit', 'Can view applications'),
                ('recruitment_admin', "Can administer the RO tool."),
                )
    def required_response_present(self, answers):
        #check for required questions
        return True
    
    def save_from_dict(self, answers):
        """
        Save question responses from POST request.
        """
        # Clear responses for checkbox type questions
        for response in self.responses.filter(question__question_type=4):
            response.response = ''
            response.save()
        for key, value in answers.items():
            split_key = key.split('-')
            if len(split_key) != 2:
                continue
            if split_key[0] == 'question':
                question_type = self.app_type.questions.get(
                        pk=int(split_key[1]))
                if self.responses.filter(question=question_type).exists():
                    response = self.responses.get(question=question_type)
                else:
                    response = AppResponse(application=self,
                            question=question_type)
                if question_type.question_type < 3:
                    response.response = answers.get(key, '')
                if question_type.question_type == 3:
                    choice_id = answers.get(key, None)
                    if not choice_id:
                        response.response = 'Unanswered'
                    else:
                        response.response = question_type.choices.get(
                                pk=int(choice_id)).value
                response.save()
            if split_key[0] == 'choice':
                choice_obj = AppQuestionChoice.objects.get(pk=int(split_key[1]))
                question_type = choice_obj.question
                if self.responses.filter(question=question_type).exists():
                    response = self.responses.get(question=question_type)
                else:
                    response = AppResponse(application=self,
                            question=question_type, response='')
                if not question_type.question_type == 4:
                    continue
                response.response = '%s%s\n' % (response.response, choice_obj.value)
                response.save()
        if not self.submitted:
            self.submitted = datetime.now(pytz.utc)
            self.save()
        return True
    
    def add_action_entries(self):
    	actions = Action.objects.filter(visible=True).all()
    	for action in actions: 
    	    if action.action_type == 1:
                result = ApprovalAction(application=self, action=action)
                result.save()
            elif action.action_type == 2:
                result = CountersignAction(application=self, action=action)
                result.save()
            else:
                result = ActionEntry(application=self, action=action)
                result.save()
        return True
        
    def can_be_accepted(self):
        if self.actionentry_set.filter(action__required=True,
                completed=False, application=self).count() != 0:
            return False
        else:
            return True
            
    def completion(self):
        """Return completion percentage for rendering"""
        action_count = float(self.actionentry_set.filter(completed=True, application=self).count())
        all_actions = float(self.actionentry_set.filter(application=self).count())
        if all_actions != 0:
            return round((float(action_count)/float(all_actions)) * 100, 1)
        else:
            return 0.0

    def add_interview(self, user, chatlog):
        result = Interview(application=self, interviewer=user,
                chatlog=chatlog)
        result.save()
        return result

    def add_comment(self, user, comment):
        result = AppComment(application=self, author=user, comment=comment)
        result.save()
        return result

    def send_applicant_mail(self, subject, body):
        # TODO: this
        return True

    def reject_application(self, user, note):
        self.disposition = 2
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        if self.app_type.disable_user_on_failure:
            self.applicant.is_active = False
            self.applicant.set_unusable_password()
            self.applicant.groups = []
            self.applicant.save()
        if self.app_type.purge_api_on_failure:
            self.applicant.api_keys.all().delete()
        self.save()
        if self.app_type.reject_mail:
            self.send_applicant_mail(subject=self.app_type.reject_subject,
                    body=self.app_type.reject_mail)
        return self

    def close_as_duplicate(self, user, note):
        self.disposition = 0
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        self.save()
        return self

    def defer_application(self, user, note):
        self.disposition = 3
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        self.save()
        if self.app_type.defer_mail:
            self.send_applicant_mail(subject=self.app_type.defer_subject,
                    body=self.app_type.defer_mail)
        return self

    def accept_application(self, user, note):
        self.disposition = 1
        self.closetime = datetime.now(pytz.utc)
        self.status_text = note
        self.closed_by = user
        if self.app_type.accept_group:
            self.applicant.groups.add(self.app_type.accept_group)
        if not self.applicant.is_active:
            self.applicant.is_active = True
            self.applicant.save()
        self.save()
        if self.app_type.accept_mail:
            self.send_applicant_mail(subject=self.app_type.accept_subject,
                    body=self.app_type.accept_mail)
        return self
        
    def reopen_app(self):
        self.disposition = None
        self.closetime = None
        self.status_text = None
        self.closed_by = None
        self.save()

    def add_workflow_entry(self, action):
        """
        Creates an empty workflow entry for the given action type.
        """
        if action.action_type == 1:
            ApprovalAction(action=action, application=self).save()
        if action.action_type == 2:
            CountersignAction(action=action, application=self).save()
        if action.action_type == 3:
            VoteAction(action=action, application=self).save()

    def recreate_workflow_entry(self, action):
        """
        Removes and re-creates the workflow entry for the given action type.
        """
        self.actions.filter(action=action).delete()
        self.add_workflow_entry(action)

    def remove_workflow_entry(self, action):
        """
        Removes the workflow entry for the given action type.
        """
        self.actions.filter(action=action).delete()

    def __unicode__(self):
        return 'Applicant: %s Status: %s' % (self.applicant.username,
                self.disposition)


class AppVote(models.Model):
    """Represents a vote on an application"""
    application = models.ForeignKey(Application, related_name='votes')
    vote = models.ForeignKey(User, related_name='appvotes')
    disposition = models.IntegerField(choices=((1,'Accept',), (2,'Reject'),
        (3, 'Defer')))
    note = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):
    """Represents an interview for an application."""
    application = models.ForeignKey(Application, related_name='interviews')
    interviewer = models.ForeignKey(User, related_name='interviews')
    chatlog = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class AppQuestion(models.Model):
    """Represents a question to be asked on the application."""
    question = models.CharField(max_length=255)
    question_type = models.IntegerField(choices=((1,'Text Field'),
        (2, 'Text Box'), (3, 'Radio'), (4, 'Checkbox')))
    description = models.TextField(null=True, blank=True)
    required = models.BooleanField(default=True)
    app_type = models.ForeignKey('AppType', related_name='questions')
    app_stage = models.ForeignKey('AppStage', related_name='questions')
    order = models.IntegerField(default=1)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order',]


class AppResponse(models.Model):
    """Represents a response to a custom application question."""
    application = models.ForeignKey(Application, related_name='responses')
    question = models.ForeignKey(AppQuestion, related_name='responses')
    response = models.TextField(blank=True, null=True)


class AppQuestionChoice(models.Model):
    question = models.ForeignKey(AppQuestion, related_name='choices')
    value = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)


class AppType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    instructions = models.TextField(null=True, blank=True)
    use_standings = models.ForeignKey(Corporation,
            related_name="applications", null=True)
    # Determines what group a user accepted via this application type will
    # have. If it is null, the user's groups will not be changed
    accept_group = models.ForeignKey(Group, related_name="applications",
            null=True)
    require_account = models.BooleanField(default=False)
    disable_user_on_failure = models.BooleanField(default=False)
    purge_api_on_failure = models.BooleanField(default=False)
    required_votes = models.IntegerField(default=1)
    accept_mail = models.TextField(null=True)
    accept_subject = models.CharField(max_length=255, null=True)
    reject_mail = models.TextField(null=True)
    reject_subject = models.CharField(max_length=255, null=True)
    defer_mail = models.TextField(null=True)
    defer_subject = models.CharField(max_length=255, null=True)
    visible = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def start_application(self, user):
        """
        Returns a blank application for the user with this type.
        """
        app = Application(app_type=self, applicant=user)
        app.save()
        return app


class AppStage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    app_type = models.ForeignKey(AppType, related_name='stages')
    order = models.IntegerField(default=1)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['order',]


class StandigsRequirement(models.Model):
    """Represents a standing to be checked against applications."""
    entity = models.CharField(max_length=100)
    # If standing is null and we have a requirement record, we can interpret
    # this as requiring no standing
    standing = models.FloatField(blank=True, null=True)
    entitytype = models.IntegerField(choices=((0,'Corporation'),
        (1,'Faction')))

class RecruitRegistrationForm(EWSUserCreationForm):
    """Extends the django registration form to add fields."""
    username = forms.CharField(max_length=30, label="Username")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password:")
