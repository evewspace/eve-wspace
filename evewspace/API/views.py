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
import urllib2
import json
import base64

from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required, login_required
from django.conf import settings

from API.models import CorpAPIKey, MemberAPIKey, APIKey, APIShipLog, APICharacter, CRESTRefreshToken
from API.utils import crest_refresh_access_token, crest_access_data, crest_verify
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
def crest_login(request):
    if not settings.CREST_ENABLED:
        raise PermissionDenied
    if request.GET.get('code'): 
    
        #use code to get access & refresh token
        authorization = base64.urlsafe_b64encode(settings.CREST_CLIENT_ID + ':' + settings.CREST_SECRET_KEY)
        data = 'grant_type=authorization_code&code=' + request.GET.get('code')
        url = 'https://'+settings.CREST_LOGIN_SERVER+'/oauth/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Host': settings.CREST_LOGIN_SERVER,
            'Authorization': 'Basic '+ authorization,}
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        requested = urllib2.Request(url, data, headers)
        json_response = opener.open(requested).read()
        access_response = json.loads(json_response)
        
        #verify validity by requesting char info
        char_authorization = access_response['access_token']
        char_url = 'https://'+settings.CREST_LOGIN_SERVER+'/oauth/verify'
        char_headers = {'User-Agent': settings.CREST_USER_AGENT,
            'Host': settings.CREST_LOGIN_SERVER,
            'Authorization': 'Bearer '+ char_authorization,}
        char_requested = urllib2.Request(char_url, None, char_headers)
        char_json_response = opener.open(char_requested).read()
        
        char_response = json.loads(char_json_response)
        
        updated_values = {
            'user_id': request.user.pk,
            'refresh_token': access_response['refresh_token'],
            'access_token': access_response['access_token'],
            'valid_until': char_response["ExpiresOn"],
            'char_name': char_response["CharacterName"],
        }
        token_info = CRESTRefreshToken.objects.update_or_create(
            char_id=char_response['CharacterID'], defaults=updated_values)
        
        
        return HttpResponseRedirect('/api/crest/overview/')
    return HttpResponseRedirect('https://'+settings.CREST_LOGIN_SERVER+'/oauth/authorize/?response_type=code&redirect_uri='+settings.CREST_BASE_URL+'api/crest/login/&client_id='+ settings.CREST_CLIENT_ID +'&scope='+settings.CREST_SCOPE+'&state=') # 302

@login_required()
def crest_overview(request):
    if not settings.CREST_ENABLED:
        return TemplateResponse(request, 'crest_not_enabled.html')
    
    tokens = CRESTRefreshToken.objects.filter(user=request.user).all()
    data = []
    
    for token in tokens:
        #request scope and verify validity by requesting char info
        response = crest_verify(token)
        data.append(response)

    return TemplateResponse(request, 'crest_overview.html', {'tokens': data})
    
@login_required()
def crest_delete(request, char_id):
    CRESTRefreshToken.objects.filter(user=request.user, char_id=char_id).delete()
    
    return HttpResponseRedirect('/api/crest/overview/')
