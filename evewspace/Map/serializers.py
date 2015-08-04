from rest_framework import serializers

from models import Map, MapSystem, System


class MapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Map
        fields = (
                'url',
                'id',
                'name',
                'root',
                'truncate_allowed',
                'explicitperms',
                'systems',
                )

class MapSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MapSystem
        fields = (
                'url',
                'id',
                'map',
                'system',
                'friendlyname',
                'interesttime',
                'parentsystem',
                'display_order_priority'
                )

class SystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = System
        fields = (
                'url',
                'id',
                'name',
                'sysclass',
                'importance',
                'occupied',
                'info',
                'lastscanned',
                'npckills',
                'podkills',
                'shipkills',
                'updated',
                'first_visited',
                'last_visited'
                )
