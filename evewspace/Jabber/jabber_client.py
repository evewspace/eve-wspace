#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
            self.sent_message(mto=jid, mbody=self.msg, mtype='chat')

        self.disconnect(wait=True)
