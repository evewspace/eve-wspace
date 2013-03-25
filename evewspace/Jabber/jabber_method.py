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
from Alerts.method_base import AlertMethodBase
from models import JabberAccount, JabberSubscription

class JabberAlertMethod(AlertMethodBase):
    """
    Alert method class for handling alerts via XMPP.
    """

    def is_registered(self, user, group):
        """
        Returns True if there is a JabberSubscription for the given user/group.
        """
        if JabberSubscription.filter(user=user, group=group).count():
            return True
        else:
            return False

    def register(self, user, group):
        """
        Register the given user/group combo.
        """
        if self.is_registered(user, group):
            return True
        else:
            JabberSubscription(user=user, group=group).save()
            return True

    def unregister(self, user, group):
        """
        Remove any existing registration for the user/group combo.
        """
        if self.is_registered(user, group):
            JabberSubscription.filter(user=user, group=group).all().delete()
        return True

    def description(self):
        """
        Return a one-liner to describe the method.
        """
        return u"Recieve alerts via Jabber (XMPP)."

