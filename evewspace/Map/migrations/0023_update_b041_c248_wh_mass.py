# -*- coding: utf-8 -*-
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):
    def forwards(self, orm):
        orm.WormholeType.objects.filter(name='B041').update(maxmass=3000000000, jumpmass=1000000000)
        orm.WormholeType.objects.filter(name='C248').update(maxmass=3000000000, jumpmass=1350000000)

    def backwards(self, orm):
        orm.WormholeType.objects.filter(name='B041').update(maxmass=5000000000, jumpmass=300000000)
        orm.WormholeType.objects.filter(name='C248').update(maxmass=5000000000, jumpmass=1800000000)

    models = {
        u'Map.wormholetype': {
            'Meta': {'object_name': 'WormholeType'},
            'destination': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jumpmass': ('django.db.models.fields.BigIntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'maxmass': ('django.db.models.fields.BigIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['Map']
    symmetrical = True
