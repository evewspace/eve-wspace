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

