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
from datetime import datetime
import pytz
from collections import defaultdict
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.template.response import TemplateResponse
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import get_object_or_404
from django import forms
from core.utils import get_config
from core.models import Corporation
from core import tasks as core_tasks
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from models import *
from API.models import MemberAPIKey, APIKey
from API import cache_handler as handler
import eveapi

def applicant_register(request, app_type=None):
    email_required = get_config('RECRUIT_REQUIRE_EMAIL', None).value == "1"
    if not app_type:
        app_type = get_object_or_404(AppType, pk=request.POST.get('app_type'))
    if request.method == "POST":
        form = RecruitRegistrationForm(request.POST)
        valid = form.is_valid()
        email = request.POST.get('email', None)
        if email_required and not email:
            form.errors['__all__'] = form.error_class(
                    ['An email address is required.'])
            valid = False
        if valid:
            newUser = form.save()
            newUser.is_active = False
            if email:
                newUser.email = email
            newUser.save()
            log_user = authenticate(username=newUser.username,
                    password=request.POST.get('password1', ''))
            login(request, log_user)
            return HttpResponseRedirect(request.POST.get('next_page'))
    else:
        form = RecruitRegistrationForm()
    next_page = reverse('Recruitment.views.get_application',
            args=(app_type.pk,))
    return TemplateResponse(request, "recruit_register.html", {'form': form,
                            'email_required': email_required,
                            'next_page': next_page,
                            'app_type': app_type.pk})


def get_application(request, app_type_id):
    app_type = get_object_or_404(AppType, pk=app_type_id)
    if app_type.require_account and not request.user.is_authenticated():
        raise PermissionDenied
    if not app_type.require_account and not request.user.is_authenticated():
        return applicant_register(request, app_type)
    app = app_type.start_application(request.user)
    return HttpResponseRedirect(
            reverse('Recruitment.views.get_application_form', args=(app.pk,)))

@login_required
def get_application_form(request, app_id):
    app = get_object_or_404(Application, pk=app_id, app_type__visible=True)
    app_type = app.app_type
    if app.applicant != request.user:
        raise PermissionDenied
    status_view = False
    if app.submitted:
        status_view = True
    stages = AppStage.objects.filter(app_type=app_type.pk, visible=True)
    questions = {}
    for stage in stages:
        questions[stage.pk] = AppQuestion.objects.filter(app_stage=stage.pk, visible=True)
    return TemplateResponse(request, 'application.html', {'app': app_type,
        'application': app, 'status_view': status_view, 'stages': stages, 'questions': questions})

@login_required
def get_api_keys(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    if app.applicant != request.user or not request.is_ajax():
        raise PermissionDenied
    if request.method == "POST":
        error_list = []
        key_id = request.POST.get('key_id', 0)
        key_vcode = request.POST.get('vcode', '')
        if not key_id or not key_vcode:
            error_list.append('You must provide both Key ID and vCode!')
        else:
            try:
                key_id = int(key_id)
            except ValueError:
               error_list.append('The Key ID is invalid (not an integer)!')
            api_key = MemberAPIKey(keyid=key_id, vcode=key_vcode,
                    user=request.user)
            api_key.validate()
            if not api_key.validation_error:
                return HttpResponse()
            else:
                error_list.append(api_key.validation_error)
                api_key.delete()
        if error_list:
            error_text = ''
            for x in error_list:
                error_text += '%s<br />' % x
            return HttpResponse(error_text, status=400)
    else:

        return TemplateResponse(request, 'api_widget.html',
                {'application': app})

@login_required
def save_application(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    if not app.required_response_present(request.POST.copy()):
        raise "Not all required questions were answered"
    try:
        app.save_from_dict(request.POST.copy())
        app.add_action_entries()
    except Exception as ex:
        raise
    return HttpResponse()

@permission_required('Recruitment.can_recruit')
def view_applications(request):
    apps = Application.objects.filter(submitted__isnull=False,
            disposition__isnull=True).all()
    return TemplateResponse(request, 'ro_panel.html', {'apps': apps})

@permission_required('Recruitment.can_recruit')
def search_applications(request):
    search = True
    filter_text = request.POST.get('filter', "")
    if request.method == "POST":
        if filter_text:
            apps = Application.objects.filter(submitted__isnull=False,
                    disposition__isnull=False, applicant__username__icontains=filter_text).order_by('-closetime').all()
        else:
            apps = Application.objects.filter(submitted__isnull=False,
                disposition__isnull=False).order_by('-closetime').all()[:20]
        return TemplateResponse(request, 'recruiter_applications.html', {'apps': apps, 'search': search})
    else:
        apps = Application.objects.filter(submitted__isnull=False,
                disposition__isnull=False).order_by('-closetime').all()[:20]
    	return TemplateResponse(request, 'ro_panel.html', {'apps': apps, 'search': search})
    
@permission_required('Recruitment.can_recruit')
def recruiter_api_key(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    if app.closetime: 
        raise PermissionDenied
    api_keys = app.applicant.api_keys.all()
    return TemplateResponse(request, "recruiter_manage_keys.html",
            {'api_keys': api_keys, 'app': app})
            
@permission_required('Recruitment.can_recruit')
def recruiter_api_key_delete(request, app_id, key_id):
    if not request.is_ajax():
        raise PermissionDenied
    api_key = get_object_or_404(MemberAPIKey, keyid=key_id)
    app = get_object_or_404(Application, pk=app_id)
    auto_comment = "An API (%s) was deleted by %s" % (key_id, request.user)
    app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
    api_key.delete()
    return HttpResponse()

@permission_required('Recruitment.can_recruit')
def recruiter_api_key_edit(request, app_id, key_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    if request.method == 'GET':
        api_key = get_object_or_404(MemberAPIKey, keyid=key_id)
    else:
        key_id = int(request.POST.get('Recruiter_key_id', None).replace(' ',''))
        vcode = request.POST.get('Recruiter_vcode', None).replace(' ', '')
        try:
            api_key = MemberAPIKey.objects.get(keyid=key_id, user=app.applicant)
            api_key.keyid = key_id
            api_key.vcode = vcode
            api_key.user = app.applicant
            api_key.validate()
        except:
            api_key = MemberAPIKey(user=app.applicant,
                            keyid=key_id,
                            vcode=vcode)
            api_key.validate()
            auto_comment = "An API (%s) was added by %s" % (key_id, request.user)
            app_comment = AppComment(application=app, author=request.user, comment=auto_comment)


    return TemplateResponse(request, "recruiter_api_key_form.html", {'key': api_key,
        'app': app})
        
@permission_required('Recruitment.can_recruit')
def recruiter_interviews(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    return TemplateResponse(request, "recruiter_interviews.html", {
        'app': app})
        
@permission_required('Recruitment.can_recruit')
def recruiter_interview_add(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    chatlog = request.POST.get('interview', None)
    if chatlog:
        app.add_interview(request.user, chatlog)
        auto_comment = "An interview was added by %s" % (request.user)
        app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
        app_comment.save()
    return HttpResponse()
        
@permission_required('Recruitment.can_recruit')
def recruiter_interview_delete(request, app_id, interview_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    #TO DO ~ Maarten
    return HttpResponse()

@permission_required('Recruitment.can_recruit')
def recruiter_get_questions(request, app_id):
    app = get_object_or_404(Application, pk=app_id)
    responses = AppResponse.objects.filter(application=app).order_by('question__app_stage__order', 'question__order')
    return TemplateResponse(request, "recruiter_questions.html", {
        'app': app, 'responses': responses})
        
@permission_required('Recruitment.can_recruit')
def recruiter_get_standings(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    standings_data = {}
    for key in app.applicant.api_keys.all():
        auth = key.get_authenticated_api()
        characters_list = auth.account.Characters()
        for character in characters_list.characters:
            char_api_standings = auth.char.Standings(characterID=character.characterID)
            char_npc_standings = char_api_standings.characterNPCStandings.NPCCorporations
            standings_test = char_npc_standings.Get(app.app_type.use_standings.pk, None)
            if standings_test:
                if standings_test.standing < 8:
                    standings_data[character.name] = True
                else:
                    standings_data[character.name] = False
            else:
                standings_data[character.name] = None
    return TemplateResponse(request, "recruiter_standings.html", {
        'app': app, 'standings_data': standings_data})

@permission_required('Recruitment.can_recruit')
def recruiter_action(request, app_id, action_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    action = get_object_or_404(Action, pk=action_id)
    
    if action.action_type == 1:
        approve_action = get_object_or_404(ApprovalAction, action=action_id, application=app_id)
        if request.method == 'POST':
            comment = request.POST.get('actionComment', None)
            approve_action.approver=request.user
            approve_action.approval_comment=comment
            approve_action.approval_time=datetime.now(pytz.utc)
            approve_action.save()
            auto_comment = "%s was signed off by %s: %s" % (approve_action.action.name, request.user, comment)
            app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
            app_comment.save()
        return TemplateResponse(request, "recruiter_approval_action.html", {
        'app': app, 'approve_action': approve_action})
    elif action.action_type == 2:
        countersign_action = get_object_or_404(CountersignAction, action=action_id, application=app_id)
        if request.method == 'POST':
            signoff_type = request.POST.get('signoff_type', None)
            if signoff_type == 'signoff':
                comment = request.POST.get('actionComment', None)
                auto_comment = "%s was signed off by %s: %s" % (countersign_action.action.name, request.user, comment)
                if request.user != countersign_action.approver2:
                    countersign_action.approver1=request.user
                    countersign_action.approver1_comment=comment
                    countersign_action.approver1_time=datetime.now(pytz.utc)
                    countersign_action.save()
            elif signoff_type == 'counter':
                comment = request.POST.get('actionComment2', None)
                auto_comment = "%s was counter signed off by %s: %s" % (countersign_action.action.name, request.user, comment)
                if request.user != countersign_action.approver1:
                    countersign_action.approver2=request.user
                    countersign_action.approver2_comment=comment
                    countersign_action.approver2_time=datetime.now(pytz.utc)
                    countersign_action.save()
            app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
            app_comment.save()
        return TemplateResponse(request, "recruiter_countersign_action.html", {
        'app': app, 'countersign_action': countersign_action})
    else:
        action_entry = get_object_or_404(ActionEntry, action=action_id, application=app_id)
        if request.method == 'POST':
            try:
                vote = VoteActionLog.objects.get(action_entry=action_entry, voter=request.user)
            except:
                vote = None
            result = request.POST.get('actionVote', None)
            comment = request.POST.get('actionComment', None)
            if result:
                if vote: 
                    vote.result = result
                    vote.comment = comment
                    vote.save()
                else:
                    new_vote = VoteActionLog(action_entry=action_entry, voter=request.user, result=result,
                        comment=comment)
                    new_vote.save()
                auto_comment = "Action %s was voted on by %s: %s" % (action_entry.action.name, request.user, comment)
                app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
                app_comment.save()
        in_favor = VoteActionLog.objects.filter(action_entry__action=action_id, action_entry__application=app_id, result=1).count()
        if in_favor >= action_entry.action.required_votes and action_entry.completed == False:
            action_entry.completed = True
            action_entry.save()
        elif in_favor < action_entry.action.required_votes and action_entry.completed:
            action_entry.completed = False
            action_entry.save()
        return TemplateResponse(request, "recruiter_vote_action.html", {
        'app': app, 'action_entry': action_entry, 'in_favor': in_favor})

@permission_required('Recruitment.can_recruit')
def recruiter_vote(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    
    if request.method == 'POST':
        result = request.POST.get('appVote', None)
        comment = request.POST.get('appVoteComment', None)
        try:
            vote = AppVote.objects.get(application=app_id, vote=request.user)
        except:
            vote = None
        if result:
            if vote:
                vote.disposition = result
                vote.note = comment
                vote.save()
            else:
                new_vote = AppVote(application=app, vote=request.user, disposition=result,
                        note=comment)
                new_vote.save()
            if result == "1":
                result2 = "accept"
            elif result == "2":
                result2 = "reject"
            else:
                result2 = "defer"
            auto_comment = "%s voted %s on the application: %s" % (request.user, result2, comment)
            app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
            app_comment.save()
            
    accept = AppVote.objects.filter(application=app_id, disposition=1).count()
    reject = AppVote.objects.filter(application=app_id, disposition=2).count()
    defer = AppVote.objects.filter(application=app_id, disposition=3).count()
    
    return TemplateResponse(request, "recruiter_vote_app.html", {
        'app': app, 'accept': accept, 'reject': reject, 'defer': defer})

@permission_required('Recruitment.can_recruit')
def recruiter_status(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    accept = AppVote.objects.filter(application=app_id, disposition=1).count()
    reject = AppVote.objects.filter(application=app_id, disposition=2).count()
    defer = AppVote.objects.filter(application=app_id, disposition=3).count()
    
    if request.method == 'POST':
        comment = request.POST.get('appComment', None)
        if comment:
            app_comment = AppComment(application=app, author=request.user, comment=comment)
            app_comment.save()
            
    return TemplateResponse(request, "recruiter_status.html", {
        'app': app, 'accept': accept, 'reject': reject, 'defer': defer})
        
@permission_required('Recruitment.can_recruit')
def recruiter_close_app(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    accept = AppVote.objects.filter(application=app_id, disposition=1).count()
    if request.method == 'POST':
        result = request.POST.get('appClose', None)
        comment = request.POST.get('closeAppComment', None)
        if result == "0":
            app.close_as_duplicate(request.user, comment)
            result2 = "duplicate"
        elif result == "1":
            if app.can_be_accepted and accept >= app.app_type.required_votes:
                app.accept_application(request.user, comment)
                result2 = "accept"
        elif result == "2":
            app.reject_application(request.user, comment)
            result2 = "reject"
        else:
            app.defer_application(request.user, comment)
            result2 = "defer"
        auto_comment = "%s closed the application as %s: %s" % (request.user, result2, comment)
        app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
        app_comment.save()

    return TemplateResponse(request, "recruiter_close_app.html", {
        'app': app, 'accept': accept})

def recruiter_reopen_app(request, app_id):
    if not request.is_ajax():
        raise PermissionDenied
    app = get_object_or_404(Application, pk=app_id)
    app.reopen_app()
    auto_comment = "%s reopened the application" % (request.user)
    app_comment = AppComment(application=app, author=request.user, comment=auto_comment)
    app_comment.save()
    return HttpResponse()
                
@permission_required('Recruitment.recruitment_admin')
def edit_applications(request):
    return TemplateResponse(request, 'edit_applications.html',
            {'apps': AppType.objects.filter(visible=True).all()})

@permission_required('Recruitment.recruitment_admin')
def workflow_section(request):
    return TemplateResponse(request, 'edit_workflow.html')

@permission_required('Recruitment.recruitment_admin')
def workflow_list(request):
    if not request.is_ajax():
        raise PermissionDenied
    actions = Action.objects.filter(visible=True).all()
    return TemplateResponse(request, 'workflow_list.html',
                {'actions': actions})

@permission_required('Recruitment.recruitment_admin')
def add_workflow(request):
    if not request.is_ajax():
        raise PermissionDenied
    if request.method == 'POST':
        name = request.POST.get('name', None)
        description = request.POST.get('description', '')
        order = request.POST.get('order', '0')
        if order:
            order_index = int(order)
        else:
            order_index = 0
        action_type = int(request.POST.get('action_type', '1'))
        votes = request.POST.get('votes', '0')
        if votes != '':
            required_votes = int(votes)
        else:
            required_votes = 0
        required = request.POST.get('required', '0') == 'on'
        action = Action(name=name, description=description, required=required,
                order=order_index, required_votes=required_votes, action_type=action_type)
        action.save()
        for application in Application.objects.filter(disposition=None).all():
            application.add_workflow_entry(action)
        return HttpResponse()
    else:
        return TemplateResponse(request, 'add_workflow.html')
        
@permission_required('Recruitment.recruitment_admin')
def edit_workflow_action(request, step_id):
    if not request.is_ajax():
        raise PermissionDenied
    action = get_object_or_404(Action, pk=step_id)
    if request.method == 'POST':
        action = get_object_or_404(Action, pk=step_id)
    	action.visible = False
    	action.save()
    	
        name = request.POST.get('name', None)
        description = request.POST.get('description', '')
        order = request.POST.get('order', '0')
        if order:
            order_index = int(order)
        else:
            order_index = 0
        action_type = int(request.POST.get('action_type', '1'))
        votes = request.POST.get('votes', '0')
        if votes != '':
            required_votes = int(votes)
        else:
            required_votes = 0
        required = request.POST.get('required', '0') == 'on'
        action = Action(name=name, description=description, required=required,
                order=order_index, required_votes=required_votes, action_type=action_type)
        action.save()
        
        return HttpResponse()
    else:
        return TemplateResponse(request, 'edit_action_workflow.html',
        {'action': action})

@permission_required('Recruitment.recruitment_admin')
def delete_workflow_action(request, step_id):
    if not request.is_ajax():
        raise PermissionDenied
    action = get_object_or_404(Action, pk=step_id)
    action.visible = False
    action.save()
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def workflow_edit(request, workflow_id):
    return TemplateResponse(request, 'edit_workflow.html')

@permission_required('Recruitment.recruitment_admin')
def recruitment_settings(request):
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def app_global_settings(request, app_type_id):
    return HttpResponse()

def _process_stage_details_form(request, app_type, stage=None):
    if not stage:
        stage = AppStage()

    name = request.POST.get('name','')
    description = request.POST.get('description','')
    order = request.POST.get('order','')

    stage.name = name
    stage.description = description
    if order:
        stage.order = int(order)
    stage.app_type = app_type

    stage.save()

    return stage

@permission_required('Recruitment.recruitment_admin')
def add_app_stage(request, app_type_id):
    if not request.is_ajax():
        raise PermissionDenied

    app_type = get_object_or_404(AppType, pk=app_type_id)
    try:
        _process_stage_details_form(request, app_type)
        return HttpResponse()
    except Exception as ex:
        return HttpResponse(repr(ex), status=400)

@permission_required('Recruitment.recruitment_admin')
def edit_app_stage(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied

    app_type = get_object_or_404(AppType, pk=app_type_id, visible=True)
    app_stage = get_object_or_404(AppStage, pk=stage_id, visible=True)
    questions = AppQuestion.objects.filter(app_stage=stage_id, visible=True)
    
    error = ''
    if request.method == 'POST':
        try:
            _process_stage_details_form(request, app_type, app_stage)
            saved = True
        except Exception as ex:
            saved = False
            error = ex.message
    else:
        saved = False

    return TemplateResponse(request, 'stage_edit.html', {'stage': app_stage,
        'saved': saved, 'error': error, 'questions': questions})

@permission_required('Recruitment.recruitment_admin')
def delete_app_type(request, app_type_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_type.visible = False
    app_type.save()
    return HttpResponse()

@permission_required('Recruitment.recruitment_admin')
def delete_app_stage(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_stage = get_object_or_404(AppStage, pk=stage_id)
    app_stage.visible = False
    app_stage.save()
    return HttpResponse()

def _process_question_form(request, app_type, stage, question=None):
    if not question:
        question = AppQuestion()
    question_text = request.POST.get('question', None)
    question_type = request.POST.get('type', None)
    order = request.POST.get('order', 1)
    question_choices = request.POST.get('choices', None)
    required = request.POST.get('required', False) != False
    description = request.POST.get('description', None)

    question.question = question_text
    question.question_type = int(question_type)
    question.app_type = app_type
    question.app_stage = stage
    if order:
        question.order = int(order)
    question.required = required
    question.description = description

    question.save()
    if question.question_type > 2:
        choices = question_choices.splitlines()
        question.choices.all().delete()
        for item in choices:
           AppQuestionChoice(question=question, value=item).save()

    return question

@permission_required('Recruitment.recruitment_admin')
def new_question(request, app_type_id, stage_id):
    if not request.is_ajax():
        raise PermissionDenied
    if request.method != "POST":
        return HttpResponse()

    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_stage = get_object_or_404(AppStage, pk=stage_id)

    try:
        question = _process_question_form(request, app_type, app_stage)
        return HttpResponse()
    except AttributeError as ex:
        return HttpResponse(ex.message, status=400)


@permission_required('Recruitment.recruitment_admin')
def edit_question(request, app_type_id, stage_id, question_id):
    if not request.is_ajax():
        raise PermissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id)
    app_stage = get_object_or_404(AppStage, pk=stage_id)
    question = get_object_or_404(AppQuestion, pk=question_id)
    if request.method != "POST":
        return TemplateResponse(request, 'edit_question.html',
                {'question': question})
    try:
        question.visible = False
        question.save()
        question = _process_question_form(request, app_type, app_stage)
        return HttpResponse()
    except Exception as ex:
        return HttpResponse(ex.message, status=400)


@permission_required('Recruitment.recruitment_admin')
def delete_question(request, app_type_id, stage_id, question_id):
    if not request.is_ajax():
        raise PermissionDenid
    if request.method != "POST":
        return HttpResponse(status=400)
    question = get_object_or_404(AppQuestion, pk=question_id)
    question.visible = False
    question.save()
    return HttpResponse()

def _process_app_type_form(request, app_type=None):
    if not app_type:
        app_type = AppType()
    name = request.POST.get('name', None)
    instructions = request.POST.get('instructions', '')
    disable_user = request.POST.get('disable_user', 'False') == 'on'
    purge_api = request.POST.get('purge_api', 'False') == 'on'
    require_user = request.POST.get('require_user', 'False') == 'on'
    standings_text = request.POST.get('standings', None)
    required_votes = request.POST.get('required_votes', '1')
    if standings_text:
        try:
            corp = Corporation.objects.get(name=standings_text)
        except Corporation.DoesNotExist:
            # Corp isn't in our DB, get its ID and add it
            api = eveapi.EVEAPIConnection(cacheHandler=handler)
            corpID = api.eve.CharacterID(
                    names=standings_text).characters[0].characterID
            try:
                corp = core_tasks.update_corporation(corpID, True)
            except AttributeError:
                # The corp doesn't exist
                return HttpResponse('Corp does not exist!', status=404)
        else:
            # Have the async worker update the corp just so that it is up to date
            core_tasks.update_corporation.delay(corp.id)
        standings_corp = get_object_or_404(Corporation,
                name=standings_text)
    else:
        standings_corp = None
    accept_text = request.POST.get('accept_group', None)
    if accept_text:
        accept_group = get_object_or_404(Group, name=accept_text)
    else:
        accept_group = None
    accept_subject = request.POST.get('accept_sbj', None)
    accept_body = request.POST.get('accept_mail', None)
    defer_subject = request.POST.get('defer_sbj', None)
    defer_body = request.POST.get('defer_mail', None)
    reject_subject = request.POST.get('reject_sbj', None)
    reject_body = request.POST.get('reject_mail', None)

    if name:
        if name != app_type.name and AppType.objects.filter(
                name=name).exists():
            raise AttributeError('The name must be unique!')
        app_type.name = name
    else:
        raise AttributeError('Name cannot be blank.')

    app_type.instructions = instructions
    app_type.use_standings = standings_corp
    app_type.accept_group = accept_group
    app_type.required_votes = required_votes
    app_type.require_account = require_user
    app_type.disable_user_on_failure = disable_user
    app_type.purge_api_on_failure = purge_api
    app_type.accept_subject = accept_subject
    app_type.accept_mail = accept_body
    app_type.defer_subject = defer_subject
    app_type.defer_mail = defer_body
    app_type.reject_subject = reject_subject
    app_type.reject_mail = reject_body
    app_type.save()

    return app_type


@permission_required('Recruitment.recruitment_admin')
def edit_app_type(request, app_type_id):
    if not request.is_ajax():
        raise PermmissionDenied
    app_type = get_object_or_404(AppType, pk=app_type_id, visible=True)
    stages = AppStage.objects.filter(app_type=app_type.pk, visible=True)
    error = None
    if request.method == "POST":
        try:
            app_type = _process_app_type_form(request, app_type)
            saved = True
        except AttributeError as ex:
           saved = False
           error = ex.message
    else:
        saved = False
    return TemplateResponse(request, 'application_edit.html',
            {'application': app_type, 'app_saved': saved, 'stages': stages, 'error': error})

@permission_required('Recruitment.recruitment_admin')
def new_app_type(request):
    if not request.is_ajax():
        raise PermissionDenied
    if request.method == "POST":
        try:
            app_type = _process_app_type_form(request)
        except AttributeError as ex:
            return HttpResponse(ex.message, status=400)
        return HttpResponse()
    else:
        return HttpResponse()
