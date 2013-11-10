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

import profile_section_registry
import user_admin_section_registry
import group_admin_section_registry

profile_section_registry.autodiscover()
group_admin_section_registry.autodiscover()
user_admin_section_registry.autodiscover()

userpatterns = patterns('account.views',
        url(r'^$', 'user_edit'),
        url(r'^profile/$', 'profile_admin'),
        url(r'^delete/$', 'delete_user'),
        url(r'^groups/$', 'user_group_list'),
        )

grouppatterns = patterns('account.views',
        url(r'^$', 'group_edit'),
        url(r'^profile/$', 'group_profile_admin'),
        url(r'^delete/$', 'delete_group'),
        url(r'^disableusers/$', 'disable_group_users'),
        url(r'^enableusers/$', 'enable_group_users'),
        url(r'^user/(?P<user_id>\d+)/add/$', 'add_group_user'),
        url(r'^user/(?P<user_id>\d+)/remove/$', 'remove_user'),)


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register/$', 'account.views.register', name='register'),
    url(r'^profile/$', 'account.views.edit_profile'),
    url(r'^admin/user/$', 'account.views.user_admin'),
    url(r'^admin/user/list/(?P<page_number>\d+)/$',
        'account.views.user_list'),
    url(r'^admin/group/$', 'account.views.group_admin'),
    url(r'^admin/group/new/$', 'account.views.create_group'),
    url(r'^admin/group/list/(?P<page_number>\d+)/$',
        'account.views.group_list'),
    url(r'^admin/user/(?P<user_id>\d+)/', include(userpatterns)),
    url(r'^admin/group/(?P<group_id>\d+)/', include(grouppatterns)),
    url(r'^password/reset$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'password_reset.html',
         'email_template_name': 'password_reset_email.html',
         'subject_template_name': 'reset_subject.txt'}, name='password_reset'),
    url(r'^password/reset/done$', 'django.contrib.auth.views.password_reset_done',
        {'template_name': 'password_reset_done.html'}, name='password_reset_done'),
    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)',
        'account.views.password_reset_confirm',
        name='password_reset_confirm'),
)
