#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from Map.models import Map
from django.template.response import TemplateResponse

# Create your views here.

@login_required()
def home_view(request):
    """The home view detects whether a user has a default map and either
    directs them to that map or displays a home page template."""

    return TemplateResponse(request, 'home.html')


@login_required
def config_view(request):
    """
    Gets the configuration page.
    """
    return TemplateResponse(request, 'settings.html')
