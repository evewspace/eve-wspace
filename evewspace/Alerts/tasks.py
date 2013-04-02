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
from celery import task
from Alerts.models import SubscriptionGroup
from Alerts import method_registry
from django.contrib.auth.models import User

@task
def send_alert(from_user, sub_group, message, subject):
    """
    Send an alert through all methods for sub_group.
    """
    # Validate permissions
    if not sub_group.get_user_perms(from_user)[0]:
        raise AttributeError("User does not have broadcast permissions.")
    else:
        # Build list of users who are eligible to recieve alerts
        to_list = []
        if not method_registry.registry:
            method_registry.autodiscover()
        for user in User.objects.filter(is_active=True):
            if user.has_perm('Alerts.can_alert'):
                to_list.append(user)
        for method in method_registry.registry:
            method_registry.registry[method]().send_alert(to_list, subject, message,
                    from_user, sub_group)
        return method_registry.registry
