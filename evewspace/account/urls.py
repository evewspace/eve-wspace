from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('', 
        url(r'^login/$', 'django.contrib.auth.views.login', 
            {'template_name': 'login.html'}, name='login'),
        url(r'^register/$', 'account.views.register', name='register'),)
