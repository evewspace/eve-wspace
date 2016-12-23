#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from datetime import datetime
import pytz

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings

from API.models import CorpAPIKey, MemberAPIKey, APIKey, APIShipLog, APICharacter, SSORefreshToken, SSOAccessList
from API.utils import sso_refresh_access_token, crest_access_data, sso_verify, esi_access_data, sso_util_login
import API.cache_handler as handler
from core.utils import get_config
from core.models import Corporation
from core import tasks as core_tasks

import eveapi

User = get_user_model()

def api_key_dialog(request):
    if not request.is_ajax():
        raise PermissionDenied
    api_keys = request.user.api_keys.all()
    return TemplateResponse(request, "manage_keys.html",
            {'api_keys': api_keys})

def api_key_admin(request, user_id):
    if not request.is_ajax():
        raise PermissionDenied
    member = get_object_or_404(User, pk=user_id)
    return TemplateResponse(request, "api_key_admin.html",
            {'member': member})

@permission_required('API.change_corpapikey')
def api_corp_key_dialog(request):
    if not request.is_ajax():
        raise PermissionDenied
    api_keys = CorpAPIKey.objects.all()
    return TemplateResponse(request, "corp_api_admin.html",
            {'api_keys': api_keys})
            
def edit_keys(request, key_id=None, user_id=None):
    if not request.is_ajax():
        raise PermissionDenied
    if key_id:
        api_key = get_object_or_404(MemberAPIKey, keyid=key_id)
    else:
        api_key = None
    user = None
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        key_id = int(request.POST.get('key_id', None).replace(' ',''))
        user = get_object_or_404(User, pk=request.POST.get('user_id', None))
        if user != request.user and not request.user.has_perm(
                'API.add_keys'):
           raise PermissionDenied
        vcode = request.POST.get('vcode', None).replace(' ', '')
        if api_key:
            api_key.keyid = key_id
            api_key.vcode = vcode
            api_key.user = user
            api_key.validate()
        else:
            api_key = MemberAPIKey(user=user,
                            keyid=key_id,
                            vcode=vcode)
            api_key.validate()
    return TemplateResponse(request, "api_key_form.html", {'key': api_key,
        'member': user})

@permission_required('API.add_corpapikey')    
def edit_corp_keys(request, key_id=None, user_id=None):
    if not request.is_ajax():
        raise PermissionDenied
    api_key = None
    user = None
    if user_id:
        user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        key_id = int(request.POST.get('key_id', None).replace(' ',''))
        user = get_object_or_404(User, pk=request.POST.get('user_id', None))
        if user != request.user and not request.user.has_perm(
                'API.add_corpapikey'):
           raise PermissionDenied
        vcode = request.POST.get('vcode', None).replace(' ', '')
        api_key = CorpAPIKey(user=user,
                        keyid=key_id,
                        vcode=vcode)
        api_key.validate()
    return TemplateResponse(request, "corp_api_key_form.html", {'key': api_key,
        'member': user})
        
def delete_key(request, key_id, purge=False):
    if not request.is_ajax():
        raise PermissionDenied
    if purge and not request.user.has_perm('API.purge_keys'):
        raise PermissionDenied
    api_key = get_object_or_404(MemberAPIKey, keyid=key_id)
    if not api_key in request.user.api_keys.all():
        if not request.user.has_perm('API.delete_keys'):
            raise PermissionDenied
    if purge:
        for character in api_key.characters.all():
            APIShipLog.objects.filter(character__name=character.name).delete()
            character.delete()
    api_key.delete()
    return HttpResponse()

@permission_required('API.delete_corpapikey')    
def delete_corp_key(request, key_id):
    if not request.is_ajax():
        raise PermissionDenied
    api_key = get_object_or_404(CorpAPIKey, keyid=key_id)    
    api_key.delete()
    return HttpResponse()

def sso_login(request):
    if not get_config("SSO_ENABLED", None).value:
        raise PermissionDenied
    if request.GET.get('code'): 
        if request.GET.get('state') == 'api' and request.user.is_authenticated():
            code = request.GET.get('code')
            sso_util_login(request, code)
         
            return HttpResponseRedirect('/api/sso/overview/')
        if request.GET.get('state') == 'login' and get_config("SSO_LOGIN_ENABLED", None).value:
            code = request.GET.get('code')
            token = sso_util_login(request, code)
            user = token.user
            
            #manually set the backend attribute to be able to login w/o password
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('https://'+settings.SSO_LOGIN_SERVER+'/oauth/authorize/?response_type=code&redirect_uri='+get_config("SSO_BASE_URL", None).value+'api/sso/login/&client_id='+ get_config("SSO_CLIENT_ID", None).value +'&scope='+get_config("SSO_SCOPE", None).value+'&state=api') # 302

@login_required()
def sso_overview(request):
    if not get_config("SSO_ENABLED", None).value:
        return TemplateResponse(request, 'sso_not_enabled.html')
    
    tokens = SSORefreshToken.objects.filter(user=request.user, valid_until__gt='1900-01-01').all()
    data = []
    
    for token in tokens:
        #request scope and verify validity by requesting char info
        response = sso_verify(token)
        data.append(response)
        
    

    return TemplateResponse(request, 'sso_overview.html', {'tokens': data})
    
@login_required()
def sso_delete(request, char_id):
    token = SSORefreshToken.objects.get(user=request.user, char_id=char_id)
    if token.char_name == token.user.username:
        token.refresh_token = None
        token.access_token = None
        token.valid_until = None
        token.save()
    else:
        token.delete()
    
    return HttpResponseRedirect('/api/sso/overview/')

@permission_required('API.change_ssoaccesslist')
def sso_admin(request):
    if not request.is_ajax():
        raise PermissionDenied
    enabled = get_config("SSO_ENABLED", None)
    client_id = get_config("SSO_CLIENT_ID", None)
    secret_key = get_config("SSO_SECRET_KEY", None)
    base_url = get_config("SSO_BASE_URL", None)
    scope = get_config("SSO_SCOPE", None)
    user_agent = get_config("SSO_USER_AGENT", None)
    login_enabled = get_config("SSO_LOGIN_ENABLED", None)
    deactivate_accounts = get_config("SSO_DEACTIVATE_ACCOUNTS", None)
    default_group = get_config("SSO_DEFAULT_GROUP", None)
    if request.method == "POST":
        enabled.value = (request.POST['enabled'])
        base_url.value = (request.POST['base_url'])
        scope.value = (request.POST['scope'])
        user_agent.value = (request.POST['user_agent'])
        login_enabled.value = (request.POST['login_enabled'])
        deactivate_accounts.value = (request.POST['deactivate_accounts'])
        enabled.save()
        base_url.save()
        scope.save()
        user_agent.save()
        login_enabled.save()
        deactivate_accounts.save()
        if len(request.POST['client_id'])>1:
            client_id.value = (request.POST['client_id'])
            client_id.save()
        if len(request.POST['secret_key'])>1:
            secret_key.value = (request.POST['secret_key'])
            secret_key.save()
        try:
            group = Group.objects.get(name=request.POST['default_group'])
            default_group.value = (request.POST['default_group'])
            default_group.save()
        except Group.DoesNotExist:
            group = None
            
    return TemplateResponse(
        request, 'sso_settings.html',
        {'enabled': enabled.value,
         'base_url': base_url.value,
         'scope': scope.value,
         'user_agent': user_agent.value,
         'login_enabled': login_enabled.value,
         'deactivate_accounts': deactivate_accounts.value,
         'default_group': default_group.value,
         'request': request})


@permission_required('API.change_ssoaccesslist')
def sso_access_list(request):
    if not request.is_ajax():
        raise PermissionDenied
    corp_name = request.POST.get('corp', None)
    char_name = request.POST.get('char', None)
    if corp_name:
        try:
            corp = Corporation.objects.get(name=corp_name)
        except Corporation.DoesNotExist:
            # Corp isn't in our DB, get its ID and add it
            try:
                api = eveapi.EVEAPIConnection(cacheHandler=handler)
                corp_id = (api.eve.CharacterID(names=corp_name)
                           .characters[0].characterID)
                if corp_id == 0:
                    return HttpResponse('Corp does not exist!', status=404)
                corp = core_tasks.update_corporation(corp_id, True)
            except:
                # Error while talking to the EVE API
                return HttpResponse('Could not verify Corp name. Please try again later.', status=404)                
        else:
            # Have the async worker update the corp so that it is up to date
            core_tasks.update_corporation.delay(corp.id)
            
        if corp: 
            SSOAccessList.objects.create(corp=corp)
            
    if char_name:
        try:
            api = eveapi.EVEAPIConnection(cacheHandler=handler)
            char_id = (api.eve.CharacterID(names=char_name)
                       .characters[0].characterID)
            char_name = (api.eve.CharacterID(names=char_name)
                       .characters[0].name)
            if char_id == 0:
                return HttpResponse('Char does not exist!', status=404)
        except:
            # Error while talking to the EVE API
            return HttpResponse('Could not verify Char name. Please try again later.', status=404)                
            
        if char_id: 
            SSOAccessList.objects.create(char_id=char_id, char_name=char_name)
    
    corps = SSOAccessList.objects.exclude(corp__isnull=True).all()
    chars = SSOAccessList.objects.exclude(char_id__isnull=True).all()
    return TemplateResponse(
        request, 'sso_access_list.html',
        {'corps': corps, 
        'chars': chars}
        )
        

@permission_required('API.change_ssoaccesslist')
def sso_delete_access_list(request, id): 
    if not request.is_ajax():
        raise PermissionDenied
    SSOAccessList.objects.get(pk=id).delete()
    return HttpResponse()
    
def sso_frontpage_login(request):
    if not get_config("SSO_ENABLED", None).value:
        raise PermissionDenied

    return HttpResponseRedirect('https://'+settings.SSO_LOGIN_SERVER+'/oauth/authorize/?response_type=code&redirect_uri='+get_config("SSO_BASE_URL", None).value+'api/sso/login/&client_id='+ get_config("SSO_CLIENT_ID", None).value +'&scope='+get_config("SSO_SCOPE", None).value+'&state=login') # 302
