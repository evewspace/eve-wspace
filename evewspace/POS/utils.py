from django.conf import settings
from models import CorpPOS
import eveapi
from API import utils as handler


def add_status_info(poses):
    """Accepts a list of corp poses and returns a list of POSes with 
    status information attached.

    A posstatus object has the following attributes:
    itemid: the POS item id
    pos: POS object processed
    status: Status retrieved

    """
    class posstatus:
        def __init__(self, pos, status):
            self.itemid = pos.apiitemid
            self.pos = pos
            self.status = status
    api = eveapi.EVEAPIConnection(cacheHandler=handler)
    auth = api.auth(keyID=settings.API_CORP_KEY_ID, vCode=settings.API_CORP_KEY_VCODE)
    #Now that we have a corp authenticated API, let's play with some POSes
    statuslist = []
    for pos in poses:
        result = auth.corp.StarbaseDetail(itemID=pos.apiitemid)
        posstatus = posstatus(pos, result)
        statuslist.append(posstatus)

    return statuslist
