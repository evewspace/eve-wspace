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
from API.models import CRESTRefreshToken
from django.conf import settings

import pytz
import urllib2
import json
import base64

def timestamp_to_datetime(timestamp):
    """Converts a UNIX Timestamp (in UTC) to a python DateTime"""
    result = datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return result

def crest_refresh_access_token(char_id):
    refresh_token = CRESTRefreshToken.objects.get(
    		char_id=char_id)

    if refresh_token.valid_until < datetime.now(pytz.utc):
	    #use code to get access & refresh token
	    authorization = base64.urlsafe_b64encode(settings.CREST_CLIENT_ID + ':' + settings.CREST_SECRET_KEY)
	    data = 'grant_type=refresh_token&refresh_token=' + refresh_token.refresh_token
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
	     
	    refresh_token.access_token = access_response['access_token']
	    refresh_token.valid_until = char_response["ExpiresOn"] 
	    refresh_token.save()

	    refresh_token = CRESTRefreshToken.objects.get(
    		char_id=char_response['CharacterID'])

    return refresh_token
    
def crest_access_data(token, requested_url, post_data = None):
    if token.valid_until < datetime.now(pytz.utc):
        token = crest_refresh_access_token(token.char_id)
    if settings.CREST_ENABLED == False:
	    return None
    authorization = token.access_token
    url = 'https://'+settings.CREST_AUTH_SERVER+requested_url
    headers = {'User-Agent': settings.CREST_USER_AGENT,
        'Host': settings.CREST_AUTH_SERVER,
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
    
    
def crest_verify(token):
    if token.valid_until < datetime.now(pytz.utc):
        token = crest_refresh_access_token(token.char_id)
    
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    authorization = token.access_token
    url = 'https://'+settings.CREST_LOGIN_SERVER+'/oauth/verify'
    headers = {'User-Agent': settings.CREST_USER_AGENT,
        'Host': settings.CREST_LOGIN_SERVER,
        'Authorization': 'Bearer '+ authorization,}
    requested = urllib2.Request(url, None, headers)
    json_response = opener.open(requested).read()
        
    response = json.loads(json_response)
    
    if response:
       return response
    return None
