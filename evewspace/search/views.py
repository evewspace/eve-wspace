from django.http import HttpResponse, Http404
import registry

# Create your views here.

def search_view(request, search):
    """
    This view instnatiates the proper search class and returns
    the result_json as an HttpResponse.
    """
    try:
        searchClass = registry.registry[search]
    except KeyError:
        raise Http404
    return HttpResponse(searchClass(request).result_json())
