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
import base64
import requests

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings

from API.models import CorpAPIKey, MemberAPIKey, APIKey, APIShipLog, APICharacter, SSORefreshToken
from API.utils import sso_refresh_access_token, crest_access_data, sso_verify, esi_access_data
import API.cache_handler as handler

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

@login_required()
def sso_login(request):
    if not settings.SSO_ENABLED:
        raise PermissionDenied
    if request.GET.get('code'): 
    
        #use code to get access & refresh token
        authorization = base64.urlsafe_b64encode(settings.SSO_CLIENT_ID + ':' + settings.SSO_SECRET_KEY)
        payload = { 'grant_type':'authorization_code', 'code': request.GET.get('code')}
        url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Host': settings.SSO_LOGIN_SERVER,
            'Authorization': 'Basic '+ authorization,}
        r = requests.post(url, data=payload, headers=headers)
        access_response = r.json()
        
        #verify validity by requesting char info
        char_authorization = access_response['access_token']
        char_url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/verify'
        char_headers = {'User-Agent': settings.SSO_USER_AGENT,
            'Host': settings.SSO_LOGIN_SERVER,
            'Authorization': 'Bearer '+ char_authorization,}
        
        r2 = requests.get(char_url, headers=char_headers)
        char_response = r2.json()
        
        updated_values = {
            'user_id': request.user.pk,
            'refresh_token': access_response['refresh_token'],
            'access_token': access_response['access_token'],
            'valid_until': char_response["ExpiresOn"],
            'char_name': char_response["CharacterName"],
        }
        token_info = SSORefreshToken.objects.update_or_create(
            char_id=char_response['CharacterID'], defaults=updated_values)
        
        
        return HttpResponseRedirect('/api/sso/overview/')
    return HttpResponseRedirect('https://'+settings.SSO_LOGIN_SERVER+'/oauth/authorize/?response_type=code&redirect_uri='+settings.SSO_BASE_URL+'api/sso/login/&client_id='+ settings.SSO_CLIENT_ID +'&scope='+settings.SSO_SCOPE+'&state=') # 302

@login_required()
def sso_overview(request):
    if not settings.SSO_ENABLED:
        return TemplateResponse(request, 'sso_not_enabled.html')
    
    tokens = SSORefreshToken.objects.filter(user=request.user).all()
    data = []
    
    for token in tokens:
        #request scope and verify validity by requesting char info
        response = sso_verify(token)
        data.append(response)
        
    

    return TemplateResponse(request, 'sso_overview.html', {'tokens': data})
    
@login_required()
def sso_delete(request, char_id):
    SSORefreshToken.objects.filter(user=request.user, char_id=char_id).delete()
    
    return HttpResponseRedirect('/api/sso/overview/')
