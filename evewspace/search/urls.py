from django.conf.urls.defaults import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from views import search_view
urlpatterns = patterns('search.views',
        url(r'^(?P<search>[-\w]+)/$',
            csrf_exempt(search_view),
            name='search_view'),
        )
