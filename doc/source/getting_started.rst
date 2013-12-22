Getting Started
===============

Now that you have Eve W-Space installed and running, there are a few additional 
steps you should take to getting it fully up and running. These tasks will also 
introduce you to administering Eve W-Space from the server console. This guide 
assumes you have installed Eve W-Space in a virtual Python environment.

Starting the Django Shell
-------------------------

The rest of this guide, and much of the overall administrative work of using 
Eve W-Space in its current state, is done from the Django shell, a Python 
interpreter with the Django enviornment pre-loaded.

Load the Virtual Environment
............................

If you installed Eve W-Space into a virtual Python environment, you need to 
have that environment active.

:command:`$ source /home/maptool/eve-wspace/bin/activate`

Result: :command:`(eve-wspace) $`

Start the Shell
...............

Now that the virtual enviornment is active, you can start the Django shell 
using the *manage.py* program.

:command:`(eve-wspace) $ /home/maptool/eve-wspace/evewspace/manage.py shell`

That should initialize the Django shell leaving you with::

    Python 2.7.3 (default, Aug  1 2012, 05:16:07) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> 

For the rest of this guide, *>>>* will indicate something to be typed in the 
Python interpreter.

Change the Admin Registration Code
----------------------------------

The first thing you should do after installing Eve W-Space is changing the 
registration code for the *Admins* group. By default, this is set to *evewspace*.

To do this from the Django shell:::

    >>>from django.contrib.auth.models import Group
    >>>adm_group = Group.objects.get(name="Admins")
    >>>adm_group.profile.regcode = 'my_super_sekrit_regcode'
    >>>adm_group.profile.save()

To do it from the UI:::

    > Log in as an administrator
    > Go to Settings and click the Groups tab
    > Click on the Admins group to bring up the edit dialog
    > Either enter a registration code or hit the Randomize button to generate one
    > Click Save

Now the registration code for the *Admins* group is whatever you put in place 
of *my_super_sekrit_regcode*. An account created with this registration code 
will have all permissions.

Create a Group for Normal Users
-------------------------------

You probably don't want all users to have all permissions in any production 
install, so you should create another group for normal users.

From the Django shell (Note: You can skip the first line if you are using the 
same shell as the last section.)::

    >>>from django.contrib.auth.models import Group
    >>>group = Group(name="Awesome Users")
    >>>group.save()
    >>>group.profile.regcode = 'sekrit_code'
    >>>group.profile.save()
    
From the UI:::

    > Log in as an administrator
    > Go to the Settings page and click the Groups tab
    > Click the 'Add Group' button
    > Fill in the pop-up form and submit


You can give this group basic map permissions from the Map Admin panel under
the "Global Permissions" section.
