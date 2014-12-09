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
from django.core.management.base import NoArgsCommand, CommandError
from django.contrib.auth.models import Group, Permission
from account.models import GroupProfile

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        """
        Installs an admin group with registration code 'evewspace.'
        If group exists, resets registration code to 'evewspace.'
        Also ensures that the Admins group has all permissions.
        """
        if Group.objects.filter(name="Admins").count() != 0:
            admin_grp = Group.objects.get(name="Admins")
            GroupProfile.objects.filter(group=admin_grp).update(regcode='evewspace')
        else:
            admin_grp = Group(name='Admins')
            admin_grp.save()
            admin_profile = GroupProfile.objects.get(group=admin_grp)
            admin_profile.regcode = 'evewspace'
            admin_profile.save()

        # Ensure admin group has all permissions in all apps
        for perm in Permission.objects.all():
            admin_grp.permissions.add(perm)

