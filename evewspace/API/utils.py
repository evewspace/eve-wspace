from API.models import APICachedDocument
from datetime import datetime
import pytz


def store(host, path, params, doc, obj):
    """Store an API document in our cache."""
    #First remove any outdated versions of the document.
    APICachedDocument.objects.filter(host=host, params=params, path=path).delete()

    #Create a new cache entry
    newDoc = APICachedDocument(host=host, params=params, path=path,
        xml=doc, cacheduntil=timestamp_to_datetime(obj.cachedUntil))
    newDoc.save()


def retrieve(host, path, params):
    """Get an API document from our cache."""
    #Look for a valid API document in the cache, make sure it isn't stale and
    #return it.
    try:
        document = APICachedDocument.objects.get(host=host,
            path=path, params=params)
        if document.cacheduntil > datetime.utcnow().replace(tzinfo=pytz.utc):
            return document.xml
        else:
            return None
    except APICachedDocument.DoesNotExist:
        #No document found, return None and let eveapi fetch and store one.
        return None
    except APICachedDocument.MultipleObjectsReturned:
        #It shouldn't be possible for this to happen, so let's just return
        #None and let it get sorted in store()
        return None


def timestamp_to_datetime(timestamp):
    """Converts a UNIX Timestamp (in UTC) to a python DateTime"""
    result = datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    return result
