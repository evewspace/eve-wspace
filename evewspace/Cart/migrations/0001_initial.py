# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShoppingCart'
        db.create_table('Cart_shoppingcart', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('totalcost', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('itemcount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('Cart', ['ShoppingCart'])

        # Adding model 'CartItem'
        db.create_table('Cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['Cart.ShoppingCart'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cart_entries', to=orm['core.Type'])),
            ('qty', self.gf('django.db.models.fields.IntegerField')()),
            ('unitcost', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('Cart', ['CartItem'])

        # Adding model 'Request'
        db.create_table('Cart_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('originuser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cartrequests', to=orm['auth.User'])),
            ('totalcost', self.gf('django.db.models.fields.BigIntegerField')()),
            ('itemcount', self.gf('django.db.models.fields.IntegerField')()),
            ('corprequest', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('daterequested', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('datefilled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('fillcost', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('deliveredto', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('datepaid', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('filluser', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requestsfilled', to=orm['auth.User'])),
        ))
        db.send_create_signal('Cart', ['Request'])

        # Adding model 'RequestItem'
        db.create_table('Cart_requestitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['Cart.Request'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='request_entries', to=orm['core.Type'])),
            ('qty', self.gf('django.db.models.fields.IntegerField')()),
            ('unitcost', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('Cart', ['RequestItem'])


    def backwards(self, orm):
        # Deleting model 'ShoppingCart'
        db.delete_table('Cart_shoppingcart')

        # Deleting model 'CartItem'
        db.delete_table('Cart_cartitem')

        # Deleting model 'Request'
        db.delete_table('Cart_request')

        # Deleting model 'RequestItem'
        db.delete_table('Cart_requestitem')


    models = {
        'Cart.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['Cart.ShoppingCart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_entries'", 'to': "orm['core.Type']"}),
            'qty': ('django.db.models.fields.IntegerField', [], {}),
            'unitcost': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'Cart.request': {
            'Meta': {'object_name': 'Request'},
            'corprequest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'datefilled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'datepaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'daterequested': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deliveredto': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fillcost': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filluser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requestsfilled'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itemcount': ('django.db.models.fields.IntegerField', [], {}),
            'originuser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cartrequests'", 'to': "orm['auth.User']"}),
            'totalcost': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'Cart.requestitem': {
            'Meta': {'object_name': 'RequestItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'request_entries'", 'to': "orm['core.Type']"}),
            'qty': ('django.db.models.fields.IntegerField', [], {}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['Cart.Request']"}),
            'unitcost': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'Cart.shoppingcart': {
            'Meta': {'object_name': 'ShoppingCart'},
            'itemcount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'totalcost': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
        'core.marketgroup': {
            'Meta': {'object_name': 'MarketGroup', 'db_table': "'invMarketGroups'", 'managed': 'False'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'hasTypes': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'marketGroupID'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'db_column': "'marketGroupName'", 'blank': 'True'}),
            'parentgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'childgroups'", 'null': 'True', 'db_column': "'parentGroupID'", 'to': "orm['core.MarketGroup']"})
        },
        'core.type': {
            'Meta': {'object_name': 'Type', 'db_table': "'invTypes'", 'managed': 'False'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'typeID'"}),
            'marketgroup': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'types'", 'null': 'True', 'db_column': "'marketGroupID'", 'to': "orm['core.MarketGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'typeName'"}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['Cart']