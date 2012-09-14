from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

class JabberGroup(models.Model):
    """Contians the definition for Jabber broadcast groups."""
    name = models.CharField(max_length = 64)
    desc = models.CharField(max_length = 200)
    # A special jabber group is one that cannot be individually joined or left.
    special = models.BooleanField()

    class Meta:
        permissions = (("can_jabber", "Use the jabber system."), 
                         ("jabber_admin", "Modify jabber groups and rosters."),)

    def __unicode__(self):
        return self.name

class JabberGroupMember(models.Model):
    """Mapping table that relates Users to their subscriped JabberGroups."""
    group = models.ForeignKey(JabberGroup, related_name = "members")
    user = models.ForeignKey(User, related_name = "jabber_groups")

class JabberGroupPermissions(models.Model):
    """Mapping table that relates Groups to their permissions for JabberGroups."""
    usergroup = models.ForeignKey(Group, related_name = "jabber_groups")
    jabbergroup = models.ForeignKey(JabberGroup, related_name = "group_permissions")
    canbroadcast = models.BooleanField()
    canjoin = models.BooleanField()

