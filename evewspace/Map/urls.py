from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('', 
        url(r'(?P<mapID>\d+)/$', 'Map.views.get_map', name='get_map'),
        url(r'new/$', 'Map.views.create_map', name='create_map'),)
