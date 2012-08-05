from Map.models import *
import datetime
import pytz

def AddLog(user, map, action):
	"""Adds a log entry into the MapLog for a map."""
	newLog = MapLog(user=user, map=map, action=action, timestamp=datetime.datetime.utcnow().replace(tzinfo=pytz.utc))
	newLog.save()
