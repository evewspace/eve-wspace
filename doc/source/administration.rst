Administration Guide
====================

These pages have guides for accomplishing various administrative tasks from the django console.

Add permissions to a group
..........................

In this example, I will explain how to give a group permission to remove and edit POS information.

By default, groups only have permission to add POSes, not edit or remove them.

First off, you need to be in the virtual environment shell::

    source eve-wspace/bin/activate
    cd eve-wspace/evewspace
    ./manage.py shell

Next, we select the group we want to give the permission to.
You can find groups under "Settings" and then "Groups" in the mapper::

    from django.contrib.auth.models import Group, Permission
    group = Group.objects.get(name='<Group Name>')

Then, we are going to add the permissions to the group::

    perm = Permission.objects.get(codename='change_pos')
    group.permissions.add(perm)

If you like, you can repeat this process with the permission `delete_pos` to allow the group to remove POSes as well.

This also works for any other permissions. You can find all the permissions Eve W-space uses in the database under the "auth_permission" table.
Be aware, however, that by far all are documented let alone implemented.
