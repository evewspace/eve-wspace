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
from API.models import SSORefreshToken
from django.conf import settings

import pytz
import base64
import requests

def timestamp_to_datetime(timestamp):
    """Converts a UNIX Timestamp (in UTC) to a python DateTime"""
    result = datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return result

def sso_refresh_access_token(char_id):
    token = SSORefreshToken.objects.get(
    		char_id=char_id)

    if refresh_token.valid_until < datetime.now(pytz.utc):
	    #use code to get access & refresh token
	    authorization = base64.urlsafe_b64encode(settings.SSO_CLIENT_ID + ':' + settings.SSO_SECRET_KEY)
	    payload = {'grant_type': 'refresh_token', 'refresh_token': token.refresh_token}
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
	     
	    token.access_token = access_response['access_token']
	    token.valid_until = char_response["ExpiresOn"] 
	    token.save()

	    token = SSORefreshToken.objects.get(
    		char_id=char_response['CharacterID'])

    return token
    
def crest_access_data(token, requested_url, post_data = None):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)
    if settings.SSO_ENABLED == False:
	    return None
    authorization = token.access_token
    url = 'https://'+settings.CREST_SERVER+'/'+requested_url
    print url
    headers = {'User-Agent': settings.SSO_USER_AGENT,
        'Host': settings.CREST_SERVER,
        'Authorization': 'Bearer '+ authorization,}
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    requested = urllib2.Request(url, post_data, headers)
    open_page = opener.open(requested)
    header_response = open_page.info()
    json_response = open_page.read()
    response = json.loads(json_response)
    
    if response:
       return response
    return None
    
    
def sso_verify(token):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)
    
    authorization = token.access_token
    url = 'https://'+settings.SSO_LOGIN_SERVER+'/oauth/verify'
    headers = {'User-Agent': settings.SSO_USER_AGENT,
        'Host': settings.SSO_LOGIN_SERVER,
        'Authorization': 'Bearer '+ authorization,}
    
    r = requests.get(url, headers=headers)
    response = r.json()
    
    if response:
       return response
    return None
    
    
def esi_access_data(token, requested_url, call_type = None, post_data = None):
    if token.valid_until < datetime.now(pytz.utc):
        token = sso_refresh_access_token(token.char_id)

    authorization = token.access_token
    url = 'https://'+ settings.ESI_SERVER + '/' + requested_url 
    payload = {'datasource': settings.ESI_SOURCE}
    headers = {'Accept': 'application/json','Authorization': 'Bearer '+ authorization}
    r = requests.get(url, headers=headers, params=payload, timeout=1.000)
    
    print r.status_code
    
    if r.status_code in (200, 201, 202, 203):
    
        response = r.json()
        print response
        if 'error' in response:
            #should be changed later
            return None
        
        if response:
           return response
    return None



