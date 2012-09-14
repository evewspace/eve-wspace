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
    posstatus = add_status_info(poses)
    return {'posstatus': posstatus}

@register.inclusion_tag('posstatus.html')
def corpposstatus(user):
    #If we have the 'can_see_all_pos' permission, show all corp POSes.
    #If we do not, then only show those with manager = None
    if user.has_perm('POS.can_see_all_pos'):
        poses = CorpPOS.objects.all()
    else:
        poses = CorpPOS.objects.filter(manager=None)
    #Add status info and return
    posstatus = add_status_info(poses)
    return {'posstatus': posstatus}

@register.inclusion_tag('posstatus_detail.html')
def posstatusdetails(posstatus):
    return {'pos': posstatus}
