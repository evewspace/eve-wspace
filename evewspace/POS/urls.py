from django.conf.urls.defaults import patterns, include, url

pospatterns = patterns('POS.views',
        url(r'delete/$', 'remove_pos'),
        )

syspatterns = patterns('POS.views',
        url(r'add/$', 'add_pos'),
        url(r'$', 'get_pos_list'),
        )

urlpatterns = patterns('POS.views',
        url(r'(?P<sysID>\d+)/', include(syspatterns)),
        )
