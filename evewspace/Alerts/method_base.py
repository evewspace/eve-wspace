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
Base class for alert method interface.
"""

class AlertMethodBase(object):
    """
    This is a skeleton AlertMethod. It should handle the following:
        send_alert(to_users, message, from_user, sub_group)
            -Send alert to given to_users. Should handle an unregistered user
             gracefully.
        register_user(user, sub_group)
            -Register the provided user and subscription group as being handled
             by this method.
        unregister_user(user, sub_group)
            -Unregister the given user and subscription group combo
        is_registered(user, sub_group)
            -Return True if the user and subscripiton group are registered
        description()
            -Return a text description of the method
    """
    def send_alert(self, to_users, message, from_user, sub_group):
        """
        Send a message to the given user with the message text, from
        and group.
        """
        # The meat of your method goes here, checking if the user
        # is registered and actually sending the alert.
        if self.is_registered(user, sub_group):
            message = "%s \n \n FROM: %s  TO: %s" % (message,
                    from_user.username, sub_group.name)
        raise NotImplementedError(message)

    def register_user(self, user, sub_group):
        """
        Register a user / subscription group combo to recieve alerts.
        """
        # You could use a model for this
        # return True if successful
        return False

    def unregister_user(self, user, sub_group):
        """
        Unregister a user / subscription group combo.
        """
        # Undo whatever you did in register_user
        # return True if successful
        return False

    def is_registered(self, user, sub_group):
        """
        Return True if the user / group combo is registered.
        """
        return False


    def description(self, user, sub_group):
        """
        Return a one-sentence descritpion of the method for the user to see.
        """
        return u"A base alert method that hasn't been implemented"

    def is_bob_great(self):
        """
        Hail Bob.
        """
        return True
