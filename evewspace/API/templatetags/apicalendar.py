from django import template
import eveapi
from API import utils as handler
from API.utils import timestamp_to_datetime
from API.models import *
register = template.Library()


@register.inclusion_tag("apicalendar.html")
def upcomingevents(user):
    #Get api character that corresponds with user's name, otherwise default to first
    subject = None
    for key in user.apikeys.all():
        for char in key.characters.all():
            if char.name.lower() == user.username.lower():
                subject = char
    if not subject:
        try:
            subject = user.apikeys.all()[0].characters.all()[0]
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


@register.inclusion_tag("apicalendar_detail.html")
def eventdetail(event):
    return {'event': event}


@register.simple_tag()
def timestamp(timestamp):
    return timestamp_to_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S")
