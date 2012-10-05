from account.models import RegistrationForm
from account.utils import *
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.util import ErrorList
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid() == True:
            # Enforce ACCOUNT_REQUIRE_REG_CODE
            if settings.ACCOUNT_REQUIRE_REG_CODE:
                if len(get_groups_for_code(form.cleaned_data['regcode'])) != 0:
                    newUser = form.save()
                    register_groups(newUser, form.cleaned_data['regcode'])
                    return HttpResponseRedirect(reverse('login'))
                else:
                    form._errors['regcode'] = ErrorList([u'Invalid Registration Code.'])
            else:
                newUser = form.save()
                register_groups(newUser, form.cleaned_data['regcode'])
                return HttpResponseRedirect(reverse('login'))

    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return TemplateResponse(request, "register.html", context)

