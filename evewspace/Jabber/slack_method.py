from Alerts.method_base import AlertMethodBase
from core.utils import get_config
from models import SlackChannel
import json
import requests

class SlackAlertMethod(AlertMethodBase):

    def send_alert(self, to_users, subject, message, from_user, sub_group):
        
        subdomain = get_config("SLACK_SUBDOMAIN", None).value
        token = get_config("SLACK_TOKEN", None).value
        
        if self.exists(sub_group):
            
            header = from_user.username+" - "+subject
            channel = SlackChannel.objects.get(group=sub_group).channel
            destination = "https://"+subdomain+".slack.com/services/hooks/incoming-webhook?token="+token
            
            payload = {'payload':json.dumps({'channel': channel, 'username': "PingBOT", 'attachments':[{'fallback': "New alert!", 'fields':[{'title': header, 'value': message}]}]})}
            requests.post(destination, data=payload)
    
    def exists(self, group):
        """
        Returns True if there is a SlackChannel for the given group.
        """
        if SlackChannel.objects.filter(group=group).count():
            return True
        else:
            return False
        
    def description(self):
        """
        Return a one-liner to describe the method.
        """
        return u"Recieve alerts via Slack."
