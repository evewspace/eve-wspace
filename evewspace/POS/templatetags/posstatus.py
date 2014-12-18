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
from django import template
from POS.models import CorpPOS
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
