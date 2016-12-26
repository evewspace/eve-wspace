from django.conf.urls import patterns, include, url

key_patterns = patterns('API.views',
        url(r'^delete/$', 'delete_key'),
        url(r'^purge/$', 'delete_key', {'purge': True}),
        url(r'^edit/$', 'edit_keys'),
        )

sso_patterns = patterns('API.views',
        url(r'^login/$', 'sso_login'),
        url(r'^overview/$', 'sso_overview'),
        url(r'^delete/(?P<char_id>\d+)/$', 'sso_delete'),
        url(r'^frontpage/login/$', 'sso_frontpage_login'),
        url(r'^settings/$', 'sso_admin'),
        url(r'^accesslist/$', 'sso_access_list'),
        url(r'^removeaccesslist/(?P<id>\d+)/$', 'sso_delete_access_list'),
        )
        
urlpatterns = patterns('API.views',
        url(r'^key/$', 'api_key_dialog'),
        url(r'^corp_key/$', 'api_corp_key_dialog'),
        url(r'^key/new/$', 'edit_keys'),
        url(r'^corp_key/new/$', 'edit_corp_keys'),
        url(r'^key/(?P<key_id>\d+)/', include(key_patterns)),
        url(r'^corp_key/(?P<key_id>\d+)/delete/', 'delete_corp_key'),
        url(r'^user/(?P<user_id>\d+)/$', 'api_key_admin'),
        url(r'^user/(?P<user_id>\d+)/key/(?P<key_id>\d+)/$', 'edit_keys'),
        url(r'^sso/', include(sso_patterns)),
        )
