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
from django import template
from POS.models import CorpPOS
from django.contrib.auth.models import User
from POS.utils import add_status_info
register=template.Library()


@register.inclusion_tag('posstatus.html')
def myposstatus(user):
    #Get list of POSes where user is the manager
    poses = CorpPOS.objects.filter(manager=user)
    #Get status information and return
    status = add_status_info(poses)
    return {'posstatus': status}


@register.inclusion_tag('posstatus.html')
def corpposstatus(user):
    #If we have the 'can_see_all_pos' permission, show all corp POSes.
    #If we do not, then only show those with manager = None
    if user.has_perm('POS.can_see_all_pos'):
        poses = CorpPOS.objects.all()
    else:
        poses = CorpPOS.objects.filter(manager=None)
    #Add status info and return
    status = add_status_info(poses)
    return {'posstatus': status}


@register.inclusion_tag('posstatus_detail.html')
def posstatusdetails(status):
    return {'pos': status}
