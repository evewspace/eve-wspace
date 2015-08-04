from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, viewsets
from rest_framework.decorators import detail_route, list_route

from models import Map, MapSystem
from serializers import *

class MapViewSet(viewsets.ViewSet):
    model = Map
    def retrieve(self, request, pk=None):
        """
        Get a Map object.
        """
        map_obj = get_object_or_404(Map, pk=pk)
        if not map_obj.get_permission(request.user):
            raise PermissionDenied
        serializer = MapSerializer(map_obj, context={'request': request})
        return Response(serializer.data)

    def list(self, request, format=None):
        """
        Return a list of Map objects.
        """
        ret_list = []
        for candidate in Map.objects.all():
            if candidate.get_permission(request.user):
                ret_list.append(candidate)
        data = MapSerializer(ret_list, many=True, context={'request': request}).data
        return Response(data)

    @detail_route(methods=['get'])
    def systems(self, request, pk=None, format=None):
        map_obj = get_object_or_404(Map, pk=pk)
        if not map_obj.get_permission(request.user):
            raise PermissionDenied
        serializer = MapSystemSerializer(map_obj.systems.all(), many=True, context={'request': request})
        return Response(serializer.data)


class MapSystemViewSet(viewsets.ViewSet):
    model = MapSystem
    def retrieve(self, request, pk=None, format=None):
        """
        Get a MapSystem
        """
        queryset = MapSystem.objects.all()
        map_sys = get_object_or_404(MapSystem, pk=pk)
        if not map_sys.map.get_permission(request.user):
            raise PermissionDenied
        serializer = MapSystemSerializer(map_sys, context={'request': request})
        return Response(serializer.data)

class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
