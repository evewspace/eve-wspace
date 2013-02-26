# Tunnel
#
# (C) 2010 Luke Slater, Steve 'Ashcrow' Milner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Authenticate XMPP user.
"""

import logging
import os
import struct
import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, check_password, Permission
from django.conf import settings


class Command(BaseCommand):
    """
    Acts as an auth service for ejabberd through ejabberds external auth
    option. See contrib/ejabberd/ejabber.cfg for an example configuration.
    """

    help = "Runs an ejabberd auth service"

    def __init__(self, *args, **kwargs):
        """
        Creation of the ejabberd atuh bridge service.

        :Parameters:
           - `args`: all non-keyword arguments
           - `kwargs`: all keyword arguments
        """
        BaseCommand.__init__(self, *args, **kwargs)
        try:
            log_level = int(settings.TUNNEL_EJABBERD_AUTH_GATEWAY_LOG_LEVEL)
        except:
            log_level = logging.INFO
        # If we can write to the log do so, else fail back to the console
        if os.access(settings.TUNNEL_EJABBERD_AUTH_GATEWAY_LOG, os.W_OK):
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s %(levelname)s %(message)s',
                filename=settings.TUNNEL_EJABBERD_AUTH_GATEWAY_LOG,
                filemode='a')
        else:
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s %(levelname)s %(message)s',
                stream=sys.stderr)
            logging.warn(('Could not write to ' +
                settings.TUNNEL_EJABBERD_AUTH_GATEWAY_LOG +
                '. Falling back to stderr ...'))
        logging.info(('ejabberd_auth_bridge process started' +
            ' (more than one is common)'))

    def _generate_response(self, success=False):
        """
        Creates and sends a response back to the ejabberd server.

        :Parameters
           - `success`: boolean if we should respond successful or not
        """
        logging.debug('Generating a response ...')
        result = 0
        if success:
            result = 1
        logging.debug('Sending response of ' + str(result))
        sys.stdout.write(struct.pack('>hh', 2, result))
        sys.stdout.flush()
        logging.debug('Response of ' + str(result) + ' sent')

    def _handle_isuser(self, username):
        """
        Handles the isuer ejabberd command.

        :Parameters:
           - `username`: the user name to verify exists
        """
        try:
            user = User.objects.get(username=username)
            logging.debug('Found user with username ' + str(username))
            self._generate_response(True)
        except User.DoesNotExist:
            logging.debug('No username ' + str(username))
            self._generate_response(False)
        except Exception, ex:
            logging.fatal('Unhandled error: ' + str(ex))

    def _handle_auth(self, username, password):
        """
        Handles authentication of the user.

        :Parameters:
           - `username`: the username to verify
           - `password`: the password to verify with the user
        """
        logging.debug('Starting auth check')
        try:
            user = User.objects.get(username=username)
            logging.debug('Found username ' + str(username))
            if check_password(password, user.password) and user.has_perm("Jabber.can_jabber"):
                self._generate_response(True)
                logging.info(username + ' has logged in')
            else:
                self._generate_response(False)
                logging.info(username + ' failed auth')
        except User.DoesNotExist:
            logging.info(username + ' is not a valid user')
            self._generate_response(False)
        except Exception, ex:
            logging.fatal('Unhandled error: ' + str(ex))

    def handle(self, **options):
        """
        How to check if a user is valid

        :Parameters:
           - `options`: keyword arguments
        """
        try:
            # Serve forever
            while True:
                logging.debug('Loop restarting')
                # Verify the information checks out
                try:
                    logging.debug('Waiting for data')
                    length = sys.stdin.read(2)
                    size = struct.unpack('>h', length)[0]
                    logging.debug('Data is of size ' + str(size))
                    logging.debug('Attempting to read the data')
                    input = sys.stdin.read(size).split(':')
                    logging.debug('Input: ' + str(input))
                    operation = input.pop(0)
                except Exception, ex:
                    # It wasn't even in the right format if we get here ...
                    logging.debug(
                        "Data was not in the right format: " + str(ex))
                    self._generate_response(False)
                    continue
                logging.debug('Checking operation ...')
                if operation == 'auth':
                    logging.info(
                        'Auth request being processed for ' + input[1])
                    self._handle_auth(input[0], input[2])
                elif operation == 'isuser':
                    logging.info('Asked if ' + input[0] + ' is a user')
                    self._handle_isuser(input[0])
                elif operation == 'setpass':
                    logging.info('Asked if to change password for ' + input[0])
                    # Do not support this
                    self._generate_repsonse(False)
                else:
                    logging.warn('Operation "' + operation + '" unknown!')
        except KeyboardInterrupt:
            logging.debug("Received Keyboard Interrupt")
            raise SystemExit(0)

    def __del__(self):
        """
        What to do when we are shut off.
        """
        logging.info('ejabberd_auth_bridge process stopped')
