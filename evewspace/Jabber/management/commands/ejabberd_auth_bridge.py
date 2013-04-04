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
"""
Authenticate XMPP user.
"""
from struct import *
import sys
import datetime
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, check_password, Permission

from core.utils import get_config

class Command(BaseCommand):
    """
    Acts as an auth service for ejabberd through ejabberds external auth
    option. See contrib/ejabberd/ejabber.cfg for an example configuration.
    """

    help = "Runs an ejabberd auth service"

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.local_enabled = False
        # Change this to True to log requests for debug *logs may include passwords*
        self.LOGGING_ENABLED = False
        if get_config("JABBER_LOCAL_ENABLED",None).value == "1":
            self.local_enabled = True
            self.local_user = get_config("JABBER_FROM_JID", False).value.split('@')[0]
            self.local_pass = get_config("JABBER_FROM_PASSWORD", False).value
            self.space_char = get_config("JABBER_LOCAL_SPACE_CHAR", False).value

    def log(self, string):
        if self.LOGGING_ENABLED:
            with open('/tmp/evewspace-jabber-bridge.log', 'a') as f:
                f.write(str(datetime.datetime.now()) + ': ' + string + '\n')

    def isuser(self, username):
        """
        Handles the isuer ejabberd command.

        :Parameters:
           - `username`: the user name to verify exists
        """
        try:
            clean_name = username.replace(self.space_char,' ')
            user = User.objects.get(username=clean_name)
            self.log('Found user with username ' + str(username))
            return True
        except User.DoesNotExist:
            self.log('No username ' + str(username))
            return False
        except Exception, ex:
            self.log('Unhandled error: ' + str(ex))
            return False

    def auth(self, username, password):
        """
        Handles authentication of the user.

        :Parameters:
           - `username`: the username to verify
           - `password`: the password to verify with the user
        """
        self.log('Starting auth check')
	if not self.local_enabled:
            return False
        try:
            clean_name = username.replace(self.space_char,' ')
            user = User.objects.get(username=clean_name)
            self.log('Found username ' + str(clean_name))
            if user.check_password(password) and user.has_perm('Alerts.can_alert'):
                self.log(username + ' has logged in')
                return True
            else:
                self.log(username + ' failed auth')
                return False
        except User.DoesNotExist:
            if username == self.local_user and password == self.local_pass:
                return True
            else:
                self.log(username + ' is not a valid user')
                return False
        except Exception, ex:
            self.log('Unhandled error: ' + str(ex))
            return False

    def from_ejabberd(self):
        input_length = sys.stdin.read(2)
        (size,) = unpack('>h', input_length)
        return sys.stdin.read(size).split(':')

    def to_ejabberd(self, bool):
        answer = 0
        if bool:
            answer = 1
        token = pack('>hh', 2, answer)
        self.log('writing token ' + str(token) + ' to stdout')
        sys.stdout.write(token)
        sys.stdout.flush()


    def handle(self, **options):
        """
        How to check if a user is valid

        :Parameters:
           - `options`: keyword arguments
        """
        while True:
            data = self.from_ejabberd()
            self.log("Got token: %s from ejabberd." % str(data))
            success = False
            if data[0] == "auth":
                success = self.auth(data[1],  data[3])
            elif data[0] == "isuser":
                success = self.isuser(data[1])
            elif data[0] == "setpass":
                success = False
            self.to_ejabberd(success)

    def __del__(self):
        """
        What to do when we are shut off.
        """
        self.log('ejabberd_auth_bridge process stopped')
