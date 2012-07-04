from django.db import models
from django.contrib.auth.models import User
from evewspace.core.models import Type

# Create your models here.

class ShoppingCart(models.Model):
	"""Represents an active shopping cart."""
	user = models.OneToOneField(User, primary_key=True)
	totalcost = models.BigIntegerField(blank=True, null=True)
	itemcount = models.IntegerField(blank=True, null=True)

	class Meta:
		permissions = (("can_cart", "Use the cart system."),)

	def __unicode__(self):
		return u"User: %s  Items: %s  Cost: %s ISK" % (self.user.name, self.itemcount, self.totalcost)

class CartItem(models.Model):
	cart = models.ForeignKey(ShoppingCart, related_name="items")
	item = models.ForeignKey(Type, related_name="cart_entries")
	qty = models.IntegerField()
	unitcost = models.BigIntegerField()

	def __unicode__(self):
		return u"Item: %s  Qty:  %s  Unit Cost:  %s" % (self.item.name, self.qty, self.unitcost)

class Request(models.Model):
	originuser = models.ForeignKey(User, related_name="cartrequests")
	totalcost = models.BigIntegerField()
	itemcount = models.IntegerField()
	corprequest = models.BooleanField()
	daterequested = models.DateTimeField(auto_now_add=True)
	datefilled = models.DateTimeField(blank=True, null=True)
	fillcost = models.BigIntegerField(blank=True, null=True)
	deliveredto = models.TextField(blank=True, null=True)
	datepaid = models.DateTimeField(blank=True, null=True)
	filluser = models.ForeignKey(User, related_name="requestsfilled")

	class Meta:
		permissions = (("can_view_requests", "View others' requests."),)

	def __unicode__(self):
		return u"User: %s Corp: %s" % (self.originuser.name, self.corprequest)

class RequestItem(models.Model):
	request = models.ForeignKey(Request, related_name="items")
	item = models.ForeignKey(Type, related_name="request_entries")
	qty = models.IntegerField()
	unitcost = models.BigIntegerField()

	def __unicode__(self):
		return u"Item: %s  Qty:  %s  Unit Cost:  %s" % (self.item.name, self.qty, self.unitcost)
