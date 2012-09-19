from django.contrib.auth.models import User, Group
from account.models import *

def get_groups_for_code(regcode):
    """Returns a list of groups for a given registration code."""
    grouplist = []
    for group in Group.objects.all():
        if group.profile.regcode == regcode:
            grouplist.append(group)

    return grouplist

def register_groups(user, regcode):
    """Registers a user for all groups associated with a registration code."""
    grouplist = get_groups_for_code(regcode)
    if len(grouplist) != 0:
        user.groups.add(grouplist)
    return None
