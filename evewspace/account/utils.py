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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from account.models import *

User = get_user_model()

def get_groups_for_code(regcode):
    """Returns a list of groups for a given registration code."""
    grouplist = []
    for group in Group.objects.filter(profile__isnull=False).all():
        profile = GroupProfile.objects.get(group=group)
        if profile.regcode == regcode:
            grouplist.append(group)

    return grouplist

def register_groups(user, regcode):
    """Registers a user for all groups associated with a registration code."""
    grouplist = get_groups_for_code(regcode)
    if len(grouplist) != 0:
        for group in grouplist:
            user.groups.add(group)
    return None
