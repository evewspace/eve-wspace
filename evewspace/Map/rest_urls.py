from django.conf.urls import patterns, include, url
from rest_framework import routers
from rest_views import *

router = routers.DefaultRouter()
router.register('maps', MapViewSet, base_name='map')
router.register('map_systems', MapSystemViewSet, base_name='mapsystem')
router.register('systems', SystemViewSet, base_name='system')

urlpatterns = router.urls
