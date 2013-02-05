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

