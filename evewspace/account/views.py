from account.models import RegistrationForm
from account.utils import *
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid() == True:
            newUser = form.save()
            register_groups(newUser, form.cleaned_data['regcode'])
            return HttpResponseRedirect(reverse('login'))

    else:
        form = RegistrationForm()
    
    context = {'form': form}
    return TemplateResponse(request, "register.html", context)

