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
    >>>adm_prof = adm_group.profile.get()
    >>>adm_prof.regcode = 'my_super_sekrit_regcode'
    >>>adm_prof.save()

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
    >>>grp_prof = group.profile.get()
    >>>grp_prof.regcode = 'probably_less_sekrit_regcode'
    >>>grp_prof.save()


Now any user registering with the registration code 
*probably_less_sekrit_regcode* will be in the *Awesome Users* group. 

You can give this group basic map permissions from the Map Admin panel under
the "Global Permissions" section.

Set the Domain Name (for IGB Trust)
-----------------------------------

Several map features rely on Eve W-Space being run in a trusted IGB session
(although the IGB isn't required for core functions). For Eve W-Space to
automatically request IGB trust, you need to tell it what domain it will
be run as (that domain will be requested as the trusted URL).

To set this from the Django shell (make sure to use http:// or https:// 
or the IGB will complain)::

    >>>from django.contrib.sites.models import Site
    >>>Site.objects.update(domain="https://alpha.evewspace.com")
    1L

You should replace *https://alpha.evewspace.com* with whatever domain
users will use to access your instance.
