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
# Create your views here.

from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
import PyTS3
from Teamspeak.models import TeamspeakServer
from core.utils import get_config
from django.http import HttpResponse

# TODO: Change login_required to the appropriate
# permission_required when the permission UI is done

@login_required
def show_online(request):
    serversettings = TeamspeakServer.objects.get(id=1)
    try:
        server = PyTS3.ServerQuery(serversettings.host, serversettings.queryport)
        server.connect()
        server.command('login', {'client_login_name': serversettings.queryuser, 'client_login_password': serversettings.querypass})
        server.command('use', {'port': str(serversettings.voiceport)})
        server.command('clientupdate', {'client_nickname': 'evewspace'})
        clientlist = server.command('clientlist -away')
        return TemplateResponse(request, 'ts_userlist.html',{'clientlist': clientlist})
    except Exception as e:
        return HttpResponse('%s' % (e), content_type="text/plain")


@login_required
def general_settings(request):
    """
    Returns and processes the general settings section.
    """
    serversettings = TeamspeakServer.objects.get(id=1)
    saved = False
    if request.method == "POST":
        serversettings.host = request.POST['ts3hostname']
        serversettings.voiceport = int(request.POST['Port'])
        serversettings.queryuser = request.POST['QueryLoginUsername']
        if request.POST['QueryLoginPasswort'] != '':
            serversettings.querypass = request.POST['QueryLoginPasswort']
        serversettings.queryport = int(request.POST['QueryPort'])
        serversettings.save()
        saved = True

    return TemplateResponse(
        request, 'teamspeak_settings.html',
        {'ts3hostname': serversettings.host,
         'Port': serversettings.voiceport,
         'QueryLoginUsername': serversettings.queryuser,
         'QueryLoginPasswort': serversettings.querypass,
         'QueryPort': serversettings.queryport,
         'saved': saved}
    )
