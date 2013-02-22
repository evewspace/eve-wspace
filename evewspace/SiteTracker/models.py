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
from django.db import models
from django.contrib.auth.models import User
from Map.models import Map, System, MapSystem
from core.utils import get_config
from datetime import datetime
import pytz

# Create your models here.

class Fleet(models.Model):
    """Represents a SiteTracker fleet."""
    system = models.ForeignKey(System, related_name="stfleets")
    initial_boss = models.ForeignKey(User, related_name="bossfleets")
    current_boss = models.ForeignKey(User, related_name="currently_bossing")
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(blank=True, null=True)
    roles_needed = models.ManyToManyField('SiteRole', related_name="fleets_need")

    class Meta:
        permissions = (("can_sitetracker", "Use the Site Tracker system."),)

    def __unicode__(self):
        return u"MapSystem: %s Boss: %s  Started: %s  Ended: %s" % (self.name,
                self.boss.username, self.started, self.ended)

    def credit_site(self, site_type, system, boss):
        """
        Credits a site.
        """
        # Get the fleet member weighting variable and multiplier
        x = int(get_config("ST_SIZE_WEIGHT", None).value)
        n = self.members.count()
        if x > 1:
            weight_factor = x / (n + (x - 1))
        else:
            # If the factor is set to anything equal to or less than 1,
            # we will not weight the results by fleet size
            weight_factor = 1
        raw_points = SiteWeight.objects.get(site_type=site_type,
                sysclass=system.sysclass).raw_points
        site = SiteRecord(fleet=self, site_type=site_type, system=system,
                boss=boss, fleetsize=self.members.count(),
                raw_points=raw_points,
                weighted_points = raw_points * weight_factor)
        site.save()
        for user in self.members.filter(leavetime=None).all():
            site.members.add(UserSite(site=site, user=user, pending=False))
        return site

    def close_fleet(self):
        """
        Closes the SiteTracker fleet.
        """
        for member in self.members.filter(leavetime=None):
            member.leavetime = datetime.now(pytz.utc)
        self.ended = datetime.now(pytz.utc)
        self.save()

    def join_fleet(self, user):
        """
        Adds user to fleet.
        """
        if not self.members.filter(user=user, leavetime=None).count():
            u = UserLog(fleet=self, user=user).save()
        else:
            u = self.members.get(user=user, leavetime=None)
        return u

    def active_members(self):
        """
        Return a list of active members.
        """
        return self.members.filter(leavetime=None)

    def leave_fleet(self, user):
        """
        Removes user from fleet.
        """
        if self.members.count() == 1:
            # We're the only member left, close the fleet.
            self.close_fleet()
        elif self.current_boss == user:
            self.current_boss = self.members.exclude(user=user).filter(
                    leavetime=None).all()[0].user
        else:
            return UserLog.objects.filter(fleet=self,
                user=user).update(leavetime=datetime.now(pytz))


class SiteRole(models.Model):
    """Represents a role for a sitetracker fleet."""
    short_name = models.CharField(max_length=32, unique=True)
    long_name = models.CharField(max_length=255, unique=True)


class SiteType(models.Model):
    """Represents a type of site that can be credited."""
    shortname = models.CharField(max_length=8, unique=True)
    longname = models.CharField(max_length=80, unique=True)
    # Defunct site types are maintained in the databse for relational purposes but can no longer be credited
    defunct = models.BooleanField()

    def __unicode__(self):
        return self.longname


class SiteWeight(models.Model):
    """
    Represents the raw points available for a site type / system class combo
    """
    site_type = models.ForeignKey(SiteType, related_name='weights')
    sysclass = models.IntegerField(choices=[(1, "C1"), (2, "C2"), (3, "C3"),
        (4, "C4"), (5, "C5"), (6, "C6"), (7, "High Sec"), (8, "Low Sec"),
        (9, "Null Sec")])
    raw_points = models.IntegerField()


class SiteRecord(models.Model):
    """Represents the record of a site run."""
    fleet = models.ForeignKey(Fleet, related_name="sites")
    site_type = models.ForeignKey(SiteType, related_name="sitesrun")
    timestamp = models.DateTimeField(auto_now_add=True)
    system = models.ForeignKey(System, related_name="sitescompleted")
    boss = models.ForeignKey(User, related_name="sitescredited")
    fleetsize = models.IntegerField()
    raw_points = models.IntegerField()
    weighted_points = models.IntegerField()

    def __unicode__(self):
        return u"System: %s Time: %s  Type: %s" % (self.system.name, self.timestamp, self.type.shortname)


class UserSite(models.Model):
    """Represents a user's credit for a site."""
    site = models.ForeignKey(SiteRecord, related_name="members")
    user = models.ForeignKey(User, related_name="sites")
    pending = models.BooleanField()

    def approve(self):
        """
        Mark the site approved.
        """
        self.pending = False
        self.save()


class UserLog(models.Model):
    """Represents a user's sitetracker log."""
    fleet = models.ForeignKey(Fleet, related_name="members")
    user = models.ForeignKey(User, related_name="sitetrackerlogs")
    jointime = models.DateTimeField(auto_now_add=True)
    leavetime = models.DateTimeField(null=True, blank=True)


class ClaimPeriod(models.Model):
    """Represents a claim period that Users can claim against."""
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    name = models.CharField(max_length = 80)
    closetime = models.DateTimeField(blank=True, null=True)
    loothauledby = models.ForeignKey(User, related_name="loothauled", null=True, blank=True)
    lootsoldby = models.ForeignKey(User, related_name="lootsold", null=True, blank=True)
    class Meta:
        permissions = (("can_close_claims", "Close the claims period early."),
                         ("can_reopen_claims", "Reopen the claims period."),
                         ("can_haul_loot", "Mark the claim period as hauled."),
                         ("can_sell_loot", "Mark the claim period as sold."),)


    def __unicode__(self):
        return self.name

class Claim(models.Model):
    """Represents a User's claim for a claim period."""
    period = models.ForeignKey(ClaimPeriod, related_name="claims")
    user = models.ForeignKey(User, related_name="claims")
    shareclaimed = models.FloatField()
    description = models.TextField()
    bonus = models.FloatField(blank=True, null=True)

class PayoutReport(models.Model):
    """Represents a payout report and contains general information about the payout period."""
    period = models.ForeignKey(ClaimPeriod, related_name="reports")
    createdby = models.ForeignKey(User, related_name="payoutreports")
    grossprofit = models.BigIntegerField()
    datepaid = models.DateTimeField(blank=True, null=True)

class PayoutEntry(models.Model):
    """Represents an entry in the payout report."""
    report = models.ForeignKey(PayoutReport, related_name="entries")
    user = models.ForeignKey(User, related_name="payouts")
    claim = models.ForeignKey(Claim, related_name="payout")
    iskshare = models.BigIntegerField()





