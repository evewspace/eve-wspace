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
from django.core.exceptions import PermissionDenied
from datetime import datetime
from API.models import SSORefreshToken, SSOAccessList
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from core.utils import get_config
import API.cache_handler as handler

import pytz
import base64
import requests
import eveapi

User = get_user_model()

def timestamp_to_datetime(timestamp):
    """Converts a UNIX Timestamp (in UTC) to a python DateTime"""
    result = datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return result

def sso_refresh_access_token(char_id):
    token = SSORefreshToken.objects.get(
            char_id=char_id)
    if get_config("SSO_ENABLED", None).value == False:
        return None
    if token.valid_until < datetime.now(pytz.utc):
        #use code to get access & refresh token
        authorization = base64.urlsafe_b64encode(get_config("SSO_CLIENT_ID", None).value + ':' + get_config("SSO_SECRET_KEY", None).value)
        payload = {'grant_type': 'refresh_token', 'refresh_token': token.refresh_token}
        url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Host': settings.SSO_LOGIN_SERVER,
            'Authorization': 'Basic '+ authorization,}
        
        try:
            r = requests.post(url, data=payload, headers=headers)
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.HTTPError:
            return None
            
        access_response = r.json()
        
        if r.status_code in (200, 201, 202, 203):
            
            #verify validity by requesting char info
            char_authorization = access_response['access_token']
            char_url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/verify'
            char_headers = {'User-Agent': get_config("SSO_USER_AGENT", None).value,
                'Host': settings.SSO_LOGIN_SERVER,
                'Authorization': 'Bearer '+ char_authorization,}
            
            try: 
                r2 = requests.get(char_url, headers=char_headers)
            except requests.exceptions.Timeout:
                return None
            except requests.exceptions.ConnectionError:
                return None
            char_response = r2.json()
            
            if r2.status_code in (200, 201, 202, 203):
            
                token.access_token = access_response['access_token']
                token.valid_until = char_response["ExpiresOn"] 
                token.save()
        
                token = SSORefreshToken.objects.get(
                    char_id=char_response['CharacterID'])
                    
                return token
        elif r.status_code in (404, 500):
            return sso_refresh_access_token(char_id)
    return None
    
def crest_access_data(token, requested_url, post_data = None):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)
    if get_config("SSO_ENABLED", None).value == False:
        return None
    authorization = token.access_token
    url = 'https://'+settings.CREST_SERVER+'/'+requested_url
    headers = {'User-Agent': get_config("SSO_USER_AGENT", None).value,
        'Host': settings.CREST_SERVER,
        'Authorization': 'Bearer '+ authorization,}
    
    try:
        r = requests.get(url, headers=headers, timeout=1.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None
    
    response = r.json()
    
    if r.status_code in (200, 201, 202, 203):
        if response:
            return response
    return None
    
    
def sso_verify(token, headers=None):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)
    
    url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/verify'
    
    if not headers:
        authorization = token.access_token
        headers = {'User-Agent': get_config("SSO_USER_AGENT", None).value,
            'Host': settings.SSO_LOGIN_SERVER,
            'Authorization': 'Bearer '+ authorization,}
            
    try:
        r = requests.get(url, headers=headers, timeout=5.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None
    
    response = r.json()
    if r.status_code in (200, 201, 202, 203):
        if response:
            return response
    return None
    
    
def esi_access_data(token, requested_url, call_type = None, post_data = None):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)
    if not get_config("SSO_ENABLED", None).value:
        return None
    authorization = token.access_token
    url = 'https://'+ settings.ESI_SERVER + '/' + requested_url 
    payload = {'datasource': settings.ESI_SOURCE}
    headers = {'Accept': 'application/json','Authorization': 'Bearer '+ authorization}
    try:
        r = requests.get(url, headers=headers, params=payload, timeout=1.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None
    
    if r.status_code in (200, 201, 202, 203):
    
        response = r.json()
        response["token"] = token
        if 'error' in response:
            #should be changed later
            return None
        
        if response:
           return response
    return None

def esi_public_data(requested_url):
    if not get_config("SSO_ENABLED", None).value:
        return None
    url = 'https://'+ settings.ESI_SERVER + '/' + requested_url 
    payload = {'datasource': settings.ESI_SOURCE}
    headers = {'Accept': 'application/json'}
    try:
        r = requests.get(url, headers=headers, params=payload, timeout=1.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None 
    
    if r.status_code in (200, 201, 202, 203):
    
        response = r.json()
        if 'error' in response:
            #should be changed later
            return None
        
        if response:
           return response
    return None


def sso_util_login(request, code):
    #use code to get access & refresh token
    authorization = base64.urlsafe_b64encode(get_config("SSO_CLIENT_ID", None).value + ':' + get_config("SSO_SECRET_KEY", None).value)
    payload = { 'grant_type':'authorization_code', 'code': code}
    url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
        'Host': settings.SSO_LOGIN_SERVER,
        'Authorization': 'Basic '+ authorization,}
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=5.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None 
    access_response = r.json()
    
    #verify validity by requesting char info
    char_authorization = access_response['access_token']
    char_url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/verify'
    char_headers = {'User-Agent': get_config("SSO_USER_AGENT", None).value,
        'Host': settings.SSO_LOGIN_SERVER,
        'Authorization': 'Bearer '+ char_authorization,}
    
    try: 
        r2 = requests.get(char_url, headers=char_headers, timeout=5.000)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.HTTPError:
        return None 
    char_response = r2.json()
    
    if request.GET.get('state') == 'login':
        #check whether they are on the access list    
        corp_id = api_current_corp(char_response['CharacterID'])
        
        #access list cross check
        if not (sso_access_list(char_response['CharacterID'], corp_id)):
            raise PermissionDenied
        
        try:
            token = SSORefreshToken.objects.get(char_id=char_response['CharacterID'])
            user = token.user
        except SSORefreshToken.DoesNotExist:
            #register new user through SSO
            password = User.objects.make_random_password()
            username = char_response["CharacterName"]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username,
                                 password=password)
            token = SSORefreshToken.objects.create(user=user, char_id=char_response['CharacterID'], char_name=char_response["CharacterName"])
            if not get_config("SSO_DEFAULT_GROUP", None).value is None and not get_config("SSO_DEFAULT_GROUP", None).value == '':
                group = Group.objects.get(name=get_config("SSO_DEFAULT_GROUP", None).value) 
                group.user_set.add(user)
        token.refresh_token = access_response['refresh_token']
        token.access_token = access_response['access_token']
        token.valid_until = char_response["ExpiresOn"]
        token.save()
        user.is_active = True
        user.save()
    else:
        updated_values = {
            'user_id': request.user.pk,
            'refresh_token': access_response['refresh_token'],
            'access_token': access_response['access_token'],
            'valid_until': char_response["ExpiresOn"],
            'char_name': char_response["CharacterName"],
        }
        token = SSORefreshToken.objects.update_or_create(
            char_id=char_response['CharacterID'], defaults=updated_values)
    
    return token
   
def sso_access_list(char_id, corp_id):
    if SSOAccessList.objects.filter(corp__pk=corp_id).exists():
        return True
    if SSOAccessList.objects.filter(char_id=char_id).exists():
        return True
    return False
    
def api_current_corp(char_id):
    url = 'characters/' + str(char_id) + '/'
    current_corp = esi_public_data(url)
    #XML API Fallback
    if not current_corp:
        api = eveapi.EVEAPIConnection(cacheHandler=handler)
        corp_id = (api.eve.CharacterInfo(characterID=char_id)
                .corporationID)
        return corp_id
    else:
        corp_id = current_corp["corporation_id"]
        return corp_id
    return None
