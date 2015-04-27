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
from django.conf.urls import patterns, include, url

apppatterns = patterns('Recruitment.views',
        url(r'stage/new/$', 'add_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/delete/$', 'delete_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/edit/$', 'edit_app_stage'),
        url(r'stage/(?P<stage_id>\d+)/question/new/$', 'new_question'),
        url(r'stage/(?P<stage_id>\d+)/question/(?P<question_id>\d+)/$', 'edit_question'),
        url(r'stage/(?P<stage_id>\d+)/question/(?P<question_id>\d+)/delete/$', 'delete_question'),
        url(r'edit/$', 'edit_app_type'),
        url(r'settings/$', 'app_global_settings'),
        url(r'delete/$', 'delete_app_type'),
        )

recruiterpatterns = patterns('Recruitment.views',
        url(r'api/view/$', 'recruiter_api_key'),
        url(r'api/edit/(?P<key_id>\d+)/$', 'recruiter_api_key_edit'),
        url(r'api/delete/(?P<key_id>\d+)/$', 'recruiter_api_key_delete'),
        url(r'interviews/$', 'recruiter_interviews'),
        url(r'interview/add/$', 'recruiter_interview_add'),
        url(r'interview/delete/(?P<interview_id>\d+)/$', 'recruiter_interview_delete'),
        url(r'questions/$', 'recruiter_get_questions'),
        url(r'standings/$', 'recruiter_get_standings'),
        url(r'action/(?P<action_id>\d+)/$', 'recruiter_action'),
        url(r'vote/$', 'recruiter_vote'),
        url(r'status/$', 'recruiter_status'),
        url(r'close_app/$', 'recruiter_close_app'),
        url(r'reopen/$', 'recruiter_reopen_app'),
        )

urlpatterns = patterns('Recruitment.views',
        url(r'register/$', 'applicant_register'),
        url(r'application/(?P<app_id>\d+)/$', 'get_application_form'),
        url(r'application/(?P<app_id>\d+)/save/$', 'save_application'),
        url(r'application/(?P<app_id>\d+)/api/$', 'get_api_keys'),
        url(r'application/new/(?P<app_type_id>\d+)/$', 'get_application'),
        url(r'application/new/$', 'new_app_type'),
        url(r'application/(?P<app_type_id>\d+)/', include(apppatterns)),
        url(r'recruiter/(?P<app_id>\d+)/', include(recruiterpatterns)),
        url(r'applications/$', 'view_applications'),
        url(r'applications/search/$', 'search_applications'),
        url(r'appeditor/$', 'edit_applications'),
        url(r'floweditor/$', 'workflow_section'),
        url(r'workflow/$', 'workflow_list'),
        url(r'workflow/new/$', 'add_workflow'),
        url(r'workflow/edit/(?P<step_id>\d+)/$', 'edit_workflow_action'),
        url(r'workflow/delete/(?P<step_id>\d+)/$', 'delete_workflow_action'),
        url(r'workflow/(?P<workflow_id>\d+)/$', 'workflow_edit'),
        url(r'settings/$', 'recruitment_settings'),
)
