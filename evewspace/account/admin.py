from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import EWSUser
from account.models import EWSUserChangeForm, EWSUserCreationForm

class EWSUserAdmin(UserAdmin):
    form = EWSUserChangeForm
    add_form = EWSUserCreationForm

admin.site.register(EWSUser, EWSUserAdmin)
