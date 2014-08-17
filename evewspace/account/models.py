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
from django import forms
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.cache import cache
from django.conf import settings
from Map.models import Map, System
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from core.models import Tenant
import pytz
import datetime
import time
# Create your models here.

User = settings.AUTH_USER_MODEL

class EWSUserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

class EWSUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    defaultmap = models.ForeignKey(Map, related_name="defaultusers", blank=True, null=True)
    objects = EWSUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        permissions = (('account_admin', 'Administer users and groups'),)

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def update_location(self, sys_id, charid, charname, shipname, shiptype):
        """
        Updates the cached locations dict for this user.
        """
        current_time = time.time()
        user_cache_key = 'user_%s_locations' % self.pk
        user_locations_dict = cache.get(user_cache_key)
        time_threshold = current_time - (60 * 15)
        location_tuple = (sys_id, charname, shipname, shiptype, current_time)
        if user_locations_dict:
            user_locations_dict.pop(charid, None)
            user_locations_dict[charid] = location_tuple
        else:
            user_locations_dict = {charid: location_tuple}
        # Prune dict to ensure we're not carrying over stale entries
        for charid, location in user_locations_dict.items():
            if location[4] < time_threshold:
                user_locations_dict.pop(charid, None)

        cache.set(user_cache_key, user_locations_dict, 60 * 15)
        return user_locations_dict

    def tenant_permissions(self, tenant):
        roles = []
        for role in self.tenant_roles.filter(tenant=tenant).all():
            for permission in role.permissions.all():
                roles.append(permission)
        return roles

    @property
    def tenants(self):
        tenants = []
        if settings.DEFAULT_TENANT_ENABLED:
            default_tenant = Tenant.objects.get(pk=1)
            if not default_tenant in tenants:
                tenants.append(default_tenant)
        for role in self.tenant_roles.all():
            if role.tenant not in tenants:
                tenants.append(role.tenant)
        return tenants


class GroupProfile(models.Model):
    """GroupProfile defines custom fields tied to each Group record."""
    group = models.OneToOneField(Group, related_name='profile')
    description = models.CharField(max_length=200, blank=True, null=True)
    regcode = models.CharField(max_length=64, blank=True, null=True)
    visible = models.BooleanField(default=True)


def create_group_profile(sender, instance, created, **kwargs):
    """Handle group creation event and create a new group profile."""
    if created:
        GroupProfile.objects.create(group=instance)

post_save.connect(create_group_profile, sender=Group)


class EWSUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, label=_("Username"))
    class Meta:
        model = EWSUser
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            EWSUser.objects.get(username=username)
        except EWSUser.DoesNotExist:
            return username
        raise forms.ValidationError(
                self.error_messages['duplicate_username'],
                code='duplicate_username',
                )


class EWSUserChangeForm(UserChangeForm):
    class Meta:
        model = EWSUser


class RegistrationForm(EWSUserCreationForm):
    """Extends the django registration form to add fields."""
    username = forms.CharField(max_length=30, label="Username")
    email = forms.EmailField(required=False, label="E-Mail Address (Optional)")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password:")
    regcode = forms.CharField(max_length=64, label="Registration Code")

