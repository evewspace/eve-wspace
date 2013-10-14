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
# Create your views here.

from django.template.response import TemplateResponse
import PyTS3
from core.utils import get_config

def show_online(request):
    ts3hostname = get_config("TS3_HOSTNAME", None).value
    Port = get_config("TS3_PORT", None).value
    QueryLoginUsername = get_config("TS3_QUERYUSER", None).value
    QueryLoginPasswort = get_config("TS3_QUERYPASS", None).value
    QueryPort = get_config("TS3_QUERYPORT", None).value

    server = PyTS3.ServerQuery(ts3hostname, QueryPort)
    server.connect()
    server.command('login', {'client_login_name': QueryLoginUsername, 'client_login_password': QueryLoginPasswort})
    server.command('use', {'port': Port})
    server.command('clientupdate', {'client_nickname': 'evewspace'})

    clientlist = server.command('clientlist -away')
    return TemplateResponse(request, 'ts_userlist.html',{'clientlist': clientlist})