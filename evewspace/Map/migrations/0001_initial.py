# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WormholeType'
        db.create_table('Map_wormholetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
            ('maxmass', self.gf('django.db.models.fields.BigIntegerField')()),
            ('jumpmass', self.gf('django.db.models.fields.BigIntegerField')()),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('destination', self.gf('django.db.models.fields.IntegerField')()),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('Map', ['WormholeType'])

        # Adding model 'System'
        db.create_table('Map_system', (
            ('systemdata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.SystemData'], unique=True, primary_key=True)),
            ('sysclass', self.gf('django.db.models.fields.IntegerField')()),
            ('occupied', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lastscanned', self.gf('django.db.models.fields.DateTimeField')()),
            ('npckills', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('podkills', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('shipkills', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('first_visited', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_visited', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('Map', ['System'])

        # Adding model 'KSystem'
        db.create_table('Map_ksystem', (
            ('system_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Map.System'], unique=True, primary_key=True)),
            ('sov', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('jumps', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('Map', ['KSystem'])

        # Adding model 'WSystem'
        db.create_table('Map_wsystem', (
            ('system_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['Map.System'], unique=True, primary_key=True)),
            ('static1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primary_statics', null=True, to=orm['Map.WormholeType'])),
            ('static2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='secondary_statics', null=True, to=orm['Map.WormholeType'])),
            ('effect', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('Map', ['WSystem'])

        # Adding model 'Map'
        db.create_table('Map_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('root', self.gf('django.db.models.fields.related.ForeignKey')(related_name='root', to=orm['Map.System'])),
            ('explicitperms', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Map', ['Map'])

        # Adding model 'MapSystem'
        db.create_table('Map_mapsystem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(related_name='systems', to=orm['Map.Map'])),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maps', to=orm['Map.System'])),
            ('friendlyname', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('interesttime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('parentsystem', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='childsystems', null=True, to=orm['Map.MapSystem'])),
        ))
        db.send_create_signal('Map', ['MapSystem'])

        # Adding model 'Wormhole'
        db.create_table('Map_wormhole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wormholes', to=orm['Map.Map'])),
            ('top', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_wormholes', to=orm['Map.MapSystem'])),
            ('top_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['Map.WormholeType'])),
            ('top_bubbled', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('bottom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent_wormholes', null=True, to=orm['Map.MapSystem'])),
            ('bottom_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['Map.WormholeType'])),
            ('bottom_bubbled', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('time_status', self.gf('django.db.models.fields.IntegerField')()),
            ('mass_status', self.gf('django.db.models.fields.IntegerField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Map', ['Wormhole'])

        # Adding model 'SignatureType'
        db.create_table('Map_signaturetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('longname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sleeprsite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('escalatable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Map', ['SignatureType'])

        # Adding model 'Signature'
        db.create_table('Map_signature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='signatures', to=orm['Map.System'])),
            ('sigtype', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sigs', null=True, to=orm['Map.SignatureType'])),
            ('sigid', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('updated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True)),
            ('activated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('downtimes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ratscleared', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lastescalated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('Map', ['Signature'])

        # Adding model 'MapPermission'
        db.create_table('Map_mappermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mappermissions', to=orm['auth.Group'])),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(related_name='grouppermissions', to=orm['Map.Map'])),
            ('access', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Map', ['MapPermission'])

        # Adding model 'MapLog'
        db.create_table('Map_maplog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logentries', to=orm['Map.Map'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maplogs', to=orm['auth.User'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Map', ['MapLog'])

        # Adding model 'Snapshot'
        db.create_table('Map_snapshot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='snapshots', to=orm['auth.User'])),
            ('json', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('Map', ['Snapshot'])

        # Adding model 'ActivePilot'
        db.create_table('Map_activepilot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locations', to=orm['auth.User'])),
            ('charactername', self.gf('django.db.models.fields.CharField')(max_length=72)),
            ('shipname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('shiptype', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='active_pilots', to=orm['Map.System'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('Map', ['ActivePilot'])

        # Adding model 'Destination'
        db.create_table('Map_destination', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destinations', to=orm['Map.KSystem'])),
            ('capital', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('Map', ['Destination'])

        # Adding model 'SiteSpawn'
        db.create_table('Map_sitespawn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysclass', self.gf('django.db.models.fields.IntegerField')()),
            ('sigtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Map.SignatureType'])),
            ('sitename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('spawns', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Map', ['SiteSpawn'])


    def backwards(self, orm):
        # Deleting model 'WormholeType'
        db.delete_table('Map_wormholetype')

        # Deleting model 'System'
        db.delete_table('Map_system')

        # Deleting model 'KSystem'
        db.delete_table('Map_ksystem')

        # Deleting model 'WSystem'
        db.delete_table('Map_wsystem')

        # Deleting model 'Map'
        db.delete_table('Map_map')

        # Deleting model 'MapSystem'
        db.delete_table('Map_mapsystem')

        # Deleting model 'Wormhole'
        db.delete_table('Map_wormhole')

        # Deleting model 'SignatureType'
        db.delete_table('Map_signaturetype')

        # Deleting model 'Signature'
        db.delete_table('Map_signature')

        # Deleting model 'MapPermission'
        db.delete_table('Map_mappermission')

        # Deleting model 'MapLog'
        db.delete_table('Map_maplog')

        # Deleting model 'Snapshot'
        db.delete_table('Map_snapshot')

        # Deleting model 'ActivePilot'
        db.delete_table('Map_activepilot')

        # Deleting model 'Destination'
        db.delete_table('Map_destination')

        # Deleting model 'SiteSpawn'
        db.delete_table('Map_sitespawn')


    models = {
        'Map.activepilot': {
            'Meta': {'object_name': 'ActivePilot'},
            'charactername': ('django.db.models.fields.CharField', [], {'max_length': '72'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shipname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'shiptype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'active_pilots'", 'to': "orm['Map.System']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locations'", 'to': "orm['auth.User']"})
        },
        'Map.destination': {
            'Meta': {'object_name': 'Destination'},
            'capital': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destinations'", 'to': "orm['Map.KSystem']"})
        },
        'Map.ksystem': {
            'Meta': {'object_name': 'KSystem', '_ormbases': ['Map.System']},
            'jumps': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sov': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'system_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Map.System']", 'unique': 'True', 'primary_key': 'True'})
        },
        'Map.map': {
            'Meta': {'object_name': 'Map'},
            'explicitperms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root'", 'to': "orm['Map.System']"})
        },
        'Map.maplog': {
            'Meta': {'object_name': 'MapLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logentries'", 'to': "orm['Map.Map']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maplogs'", 'to': "orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Map.mappermission': {
            'Meta': {'object_name': 'MapPermission'},
            'access': ('django.db.models.fields.IntegerField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mappermissions'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grouppermissions'", 'to': "orm['Map.Map']"})
        },
        'Map.mapsystem': {
            'Meta': {'object_name': 'MapSystem'},
            'friendlyname': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interesttime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'to': "orm['Map.Map']"}),
            'parentsystem': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childsystems'", 'null': 'True', 'to': "orm['Map.MapSystem']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maps'", 'to': "orm['Map.System']"})
        },
        'Map.signature': {
            'Meta': {'ordering': "['sigid']", 'object_name': 'Signature'},
            'activated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'downtimes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'}),
            'lastescalated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ratscleared': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sigid': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sigtype': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sigs'", 'null': 'True', 'to': "orm['Map.SignatureType']"}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'signatures'", 'to': "orm['Map.System']"}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Map.signaturetype': {
            'Meta': {'object_name': 'SignatureType'},
            'escalatable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'sleeprsite': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'Map.sitespawn': {
            'Meta': {'object_name': 'SiteSpawn'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sigtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Map.SignatureType']"}),
            'sitename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spawns': ('django.db.models.fields.TextField', [], {}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {})
        },
        'Map.snapshot': {
            'Meta': {'object_name': 'Snapshot'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'snapshots'", 'to': "orm['auth.User']"})
        },
        'Map.system': {
            'Meta': {'object_name': 'System', '_ormbases': ['core.SystemData']},
            'first_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastscanned': ('django.db.models.fields.DateTimeField', [], {}),
            'npckills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'occupied': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {}),
            'systemdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SystemData']", 'unique': 'True', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'Map.wormhole': {
            'Meta': {'object_name': 'Wormhole'},
            'bottom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent_wormholes'", 'null': 'True', 'to': "orm['Map.MapSystem']"}),
            'bottom_bubbled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'bottom_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['Map.WormholeType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wormholes'", 'to': "orm['Map.Map']"}),
            'mass_status': ('django.db.models.fields.IntegerField', [], {}),
            'time_status': ('django.db.models.fields.IntegerField', [], {}),
            'top': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_wormholes'", 'to': "orm['Map.MapSystem']"}),
            'top_bubbled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'top_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['Map.WormholeType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'Map.wormholetype': {
            'Meta': {'object_name': 'WormholeType'},
            'destination': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jumpmass': ('django.db.models.fields.BigIntegerField', [], {}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {}),
            'maxmass': ('django.db.models.fields.BigIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'Map.wsystem': {
            'Meta': {'object_name': 'WSystem', '_ormbases': ['Map.System']},
            'effect': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'static1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primary_statics'", 'null': 'True', 'to': "orm['Map.WormholeType']"}),
            'static2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'secondary_statics'", 'null': 'True', 'to': "orm['Map.WormholeType']"}),
            'system_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['Map.System']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.constellation': {
            'Meta': {'object_name': 'Constellation', 'db_table': "'mapConstellations'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'constellationID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'constellationName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'constellations'", 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'mapRegions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'regionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'regionName'"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        'core.systemdata': {
            'Meta': {'object_name': 'SystemData', 'db_table': "'mapSolarSystems'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'constellationID'", 'to': "orm['core.Constellation']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'solarSystemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'solarSystemName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'regionID'", 'to': "orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['Map']