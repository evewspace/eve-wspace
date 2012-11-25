from django.conf.urls.defaults import patterns, include, url

pospatterns = patterns('POS.views',
        url(r'remove/$', 'remove_pos'),
        url(r'edit/$', 'edit_pos'),
        )

syspatterns = patterns('POS.views',
        url(r'(?P<posID>\d+)/', include(pospatterns)),
        url(r'add/$', 'add_pos'),
        url(r'$', 'get_pos_list'),
        )

urlpatterns = patterns('POS.views',
        url(r'(?P<sysID>\d+)/', include(syspatterns)),
        )
