from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('POS.views',
        url(r'(?P<posID>\d+)/testfit/$', 'test_fit'),
        )
