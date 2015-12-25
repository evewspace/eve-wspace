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
from celery import task
from Alerts.models import SubscriptionGroup
from Alerts import method_registry
from django.contrib.auth import get_user_model

User = get_user_model()

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
        results = {}
        for method in method_registry.registry:
            results[method] = method_registry.registry[method]().send_alert(
                    to_list, subject, message, from_user, sub_group)
        return results
