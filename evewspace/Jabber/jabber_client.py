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
import sleekxmpp

class JabberClient(sleekxmpp.ClientXMPP):
    """
    Jabber client for sending a list of alerts.

    Arguments:
        jid -- JID to send as
        password -- Password for send JID
        to_list -- List of JIDs to send to
        message -- Message to be sent
    """
    def __init__(self, jid, password, to_list, message):
        super(JabberClient, self).__init__(jid, password)
        self.recipient_list = to_list
        self.msg = message

        self.add_event_handler("session_start", self.start)

    def start(self, event):
        """
        Send message to each recipient and disconnect gracefully.
        """
        self.send_presence()
        self.get_roster()
        for jid in self.recipient_list:
            self.send_message(mto=jid, mbody=self.msg, mtype='chat')
        self.disconnect(wait=True)
