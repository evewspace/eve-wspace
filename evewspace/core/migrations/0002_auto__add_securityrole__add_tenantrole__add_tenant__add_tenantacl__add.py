# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SecurityRole'
        db.create_table(u'core_securityrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['SecurityRole'])

        # Adding model 'TenantRole'
        db.create_table(u'core_tenantrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tenant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='roles', to=orm['core.Tenant'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'core', ['TenantRole'])

        # Adding M2M table for field users on 'TenantRole'
        m2m_table_name = db.shorten_name(u'core_tenantrole_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tenantrole', models.ForeignKey(orm[u'core.tenantrole'], null=False)),
            ('ewsuser', models.ForeignKey(orm[u'account.ewsuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tenantrole_id', 'ewsuser_id'])

        # Adding M2M table for field permissions on 'TenantRole'
        m2m_table_name = db.shorten_name(u'core_tenantrole_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tenantrole', models.ForeignKey(orm[u'core.tenantrole'], null=False)),
            ('securityrole', models.ForeignKey(orm[u'core.securityrole'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tenantrole_id', 'securityrole_id'])

        # Adding model 'Tenant'
        db.create_table(u'core_tenant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('admin_notes', self.gf('django.db.models.fields.TextField')(null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['Tenant'])

        # Adding model 'TenantACL'
        db.create_table(u'core_tenantacl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tenant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='acl_entries', to=orm['core.Tenant'])),
            ('char_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('corp_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('alliance_id', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser'], null=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(related_name='acl_entries', to=orm['core.TenantRole'])),
        ))
        db.send_create_signal(u'core', ['TenantACL'])

        # Adding model 'Character'
        db.create_table(u'core_character', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('corporation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Corporation'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.EWSUser'], null=True)),
        ))
        db.send_create_signal(u'core', ['Character'])


        # Changing field 'ConfigEntry.user'
        db.alter_column(u'core_configentry', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))

        # Changing field 'NewsFeed.user'
        db.alter_column(u'core_newsfeed', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['account.EWSUser']))

    def backwards(self, orm):
        # Deleting model 'SecurityRole'
        db.delete_table(u'core_securityrole')

        # Deleting model 'TenantRole'
        db.delete_table(u'core_tenantrole')

        # Removing M2M table for field users on 'TenantRole'
        db.delete_table(db.shorten_name(u'core_tenantrole_users'))

        # Removing M2M table for field permissions on 'TenantRole'
        db.delete_table(db.shorten_name(u'core_tenantrole_permissions'))

        # Deleting model 'Tenant'
        db.delete_table(u'core_tenant')

        # Deleting model 'TenantACL'
        db.delete_table(u'core_tenantacl')

        # Deleting model 'Character'
        db.delete_table(u'core_character')


        # Changing field 'ConfigEntry.user'
        db.alter_column(u'core_configentry', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'NewsFeed.user'
        db.alter_column(u'core_newsfeed', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

    models = {
        u'Map.map': {
            'Meta': {'object_name': 'Map'},
            'explicitperms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'root': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'root'", 'to': u"orm['Map.System']"})
        },
        u'Map.system': {
            'Meta': {'object_name': 'System', '_ormbases': [u'core.SystemData']},
            'first_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'importance': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_visited': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'lastscanned': ('django.db.models.fields.DateTimeField', [], {}),
            'npckills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'occupied': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'podkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipkills': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {}),
            u'systemdata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.SystemData']", 'unique': 'True', 'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'account.ewsuser': {
            'Meta': {'object_name': 'EWSUser'},
            'current_tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'active_users'", 'null': 'True', 'to': u"orm['core.Tenant']"}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'defaultmap': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'defaultusers'", 'null': 'True', 'to': u"orm['Map.Map']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.alliance': {
            'Meta': {'object_name': 'Alliance'},
            'executor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['core.Corporation']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.character': {
            'Meta': {'object_name': 'Character'},
            'corporation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Corporation']", 'null': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.EWSUser']", 'null': 'True'})
        },
        u'core.configentry': {
            'Meta': {'object_name': 'ConfigEntry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'settings'", 'null': 'True', 'to': u"orm['account.EWSUser']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.constellation': {
            'Meta': {'object_name': 'Constellation', 'db_table': "'mapConstellations'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'constellationID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'constellationName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'constellations'", 'db_column': "'regionID'", 'to': u"orm['core.Region']"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.corporation': {
            'Meta': {'object_name': 'Corporation'},
            'alliance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_corps'", 'null': 'True', 'to': u"orm['core.Alliance']"}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'member_count': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.faction': {
            'Meta': {'object_name': 'Faction', 'db_table': "u'chrFactions'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'blank': 'True'}),
            'iconid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'iconID'", 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'factionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_column': "'factionName'", 'blank': 'True'})
        },
        u'core.location': {
            'Meta': {'object_name': 'Location', 'db_table': "'mapDenormalize'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'constellationID'", 'to': u"orm['core.Constellation']"}),
            'itemid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'itemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'itemName'", 'blank': 'True'}),
            'orbitparent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'satellites'", 'null': 'True', 'db_column': "'orbitID'", 'to': u"orm['core.Location']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'regionID'", 'to': u"orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'security'", 'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'solarSystemID'", 'to': u"orm['core.SystemData']"}),
            'typeid': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mapentries'", 'null': 'True', 'db_column': "'typeID'", 'to': u"orm['core.Type']"}),
            'x': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'x'", 'blank': 'True'}),
            'y': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'y'", 'blank': 'True'}),
            'z': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'z'", 'blank': 'True'})
        },
        u'core.locationwormholeclass': {
            'Meta': {'object_name': 'LocationWormholeClass', 'db_table': "'mapLocationWormholeClasses'", 'managed': 'False'},
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'whclass'", 'primary_key': 'True', 'db_column': "'locationID'", 'to': u"orm['core.Location']"}),
            'sysclass': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'wormholeClassID'", 'blank': 'True'})
        },
        u'core.marketgroup': {
            'Meta': {'object_name': 'MarketGroup', 'db_table': "'invMarketGroups'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hasTypes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'marketGroupID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'marketGroupName'", 'blank': 'True'}),
            'parentgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childgroups'", 'null': 'True', 'db_column': "'parentGroupID'", 'to': u"orm['core.MarketGroup']"})
        },
        u'core.newsfeed': {
            'Meta': {'ordering': "['name']", 'object_name': 'NewsFeed'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'null': 'True', 'to': u"orm['account.EWSUser']"})
        },
        u'core.region': {
            'Meta': {'object_name': 'Region', 'db_table': "'mapRegions'", 'managed': 'False'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'regionID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'regionName'"}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.securityrole': {
            'Meta': {'object_name': 'SecurityRole'},
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.starbaseresource': {
            'Meta': {'object_name': 'StarbaseResource', 'db_table': "'invControlTowerResources'", 'managed': 'False'},
            'minSecurityLevel': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'minSecurityLevel'", 'blank': 'True'}),
            'purpose': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'usedby'", 'null': 'True', 'db_column': "'purpose'", 'to': u"orm['core.StarbaseResourcePurpose']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'quantity'", 'blank': 'True'}),
            'resourceType': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posfuel'", 'db_column': "'resourceTypeID'", 'to': u"orm['core.Type']"}),
            'towerType': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posesfueled'", 'primary_key': 'True', 'db_column': "'controlTowerTypeID'", 'to': u"orm['core.Type']"})
        },
        u'core.starbaseresourcepurpose': {
            'Meta': {'object_name': 'StarbaseResourcePurpose', 'db_table': "'invControlTowerResourcePurposes'", 'managed': 'False'},
            'purpose': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'purposeText': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.systemdata': {
            'Meta': {'object_name': 'SystemData', 'db_table': "'mapSolarSystems'", 'managed': 'False'},
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'constellationID'", 'to': u"orm['core.Constellation']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'solarSystemID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'solarSystemName'"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'systems'", 'db_column': "'regionID'", 'to': u"orm['core.Region']"}),
            'security': ('django.db.models.fields.FloatField', [], {}),
            'x': ('django.db.models.fields.FloatField', [], {}),
            'y': ('django.db.models.fields.FloatField', [], {}),
            'z': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.systemjump': {
            'Meta': {'object_name': 'SystemJump', 'db_table': "'mapSolarSystemJumps'", 'managed': 'False'},
            'fromconstellation': ('django.db.models.fields.IntegerField', [], {'db_column': "'fromConstellationID'"}),
            'fromregion': ('django.db.models.fields.IntegerField', [], {'db_column': "'fromRegionID'"}),
            'fromsystem': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'fromSolarSystemID'"}),
            'toconstellation': ('django.db.models.fields.IntegerField', [], {'db_column': "'toConstellationID'"}),
            'toregion': ('django.db.models.fields.IntegerField', [], {'db_column': "'toRegionID'"}),
            'tosystem': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'toSolarSystemID'"})
        },
        u'core.tenant': {
            'Meta': {'object_name': 'Tenant'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'admin_notes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.tenantacl': {
            'Meta': {'object_name': 'TenantACL'},
            'alliance_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'char_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'corp_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'acl_entries'", 'to': u"orm['core.TenantRole']"}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'acl_entries'", 'to': u"orm['core.Tenant']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.EWSUser']", 'null': 'True'})
        },
        u'core.tenantrole': {
            'Meta': {'object_name': 'TenantRole'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tenant_roles'", 'symmetrical': 'False', 'to': u"orm['core.SecurityRole']"}),
            'tenant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': u"orm['core.Tenant']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tenant_roles'", 'symmetrical': 'False', 'to': u"orm['account.EWSUser']"})
        },
        u'core.type': {
            'Meta': {'object_name': 'Type', 'db_table': "'invTypes'", 'managed': 'False'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'typeID'"}),
            'marketgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'types'", 'null': 'True', 'db_column': "'marketGroupID'", 'to': u"orm['core.MarketGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'typeName'"}),
            'published': ('django.db.models.fields.BooleanField', [], {}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']