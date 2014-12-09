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
from django import template
import eveapi
from API import cache_handler as handler
from API.utils import timestamp_to_datetime
from API.models import *
register = template.Library()


@register.inclusion_tag("apicalendar.html")
def upcomingevents(user):
    #Get api character that corresponds with user's name, otherwise default to first
    subject = None
    for key in user.api_keys.all():
        for char in key.characters.all():
            if char.name.lower() == user.username.lower():
                subject = char
    if not subject:
        try:
            subject = user.api_keys.all()[0].characters.all()[0]
        except:
            return {'error': 'No API Key was found.'}

    #Retrieve calendar events. If unable, return error context.
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    auth = api.auth(keyID=char.apikey.keyid, vCode=char.apikey.vcode)
    try:
        result = auth.char.UpcomingCalendarEvents(characterID=subject.charid)
        result.upcomingEvents.SortBy('eventDate')
        return {'events': result.upcomingEvents}
    except eveapi.Error:
        return {'error': 'Your API Key does not allow calendar access.'}
    except RuntimeError:
        return {'error': 'There was a problem contacting the API server.'}


@register.inclusion_tag("apicalendar_detail.html")
def eventdetail(event):
    return {'event': event}


@register.simple_tag()
def timestamp(timestamp):
    return timestamp_to_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S")
