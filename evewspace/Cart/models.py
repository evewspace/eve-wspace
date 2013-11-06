#    Eve W-Space
#    Copyright (C) 2013  Andrew Austin and other contributors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version. An additional term under section
#    7 of the GPL is included in the LICENSE file.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
from django.db import models
from django.contrib.auth.models import User
from core.models import Type

# Create your models here.

class ShoppingCart(models.Model):
    """Represents an active shopping cart."""
    user = models.OneToOneField(User, primary_key=True)
    totalcost = models.BigIntegerField(blank=True, null=True)
    itemcount = models.IntegerField(blank=True, null=True)

    class Meta:
        permissions = (("can_cart", "Use the cart system."),)

    def __unicode__(self):
        return u"User: %s  Items: %s  Cost: %s ISK" % (self.user.username,
                self.itemcount, self.totalcost)


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name="items")
    item = models.ForeignKey(Type, related_name="cart_entries")
    qty = models.IntegerField()
    unitcost = models.BigIntegerField()

    def __unicode__(self):
        return u"Item: %s  Qty:  %s  Unit Cost:  %s" % (self.item.name,
                self.qty, self.unitcost)


class Request(models.Model):
    originuser = models.ForeignKey(User, related_name="cartrequests")
    totalcost = models.BigIntegerField()
    itemcount = models.IntegerField()
    corprequest = models.BooleanField(default=False)
    daterequested = models.DateTimeField(auto_now_add=True)
    datefilled = models.DateTimeField(blank=True, null=True)
    fillcost = models.BigIntegerField(blank=True, null=True)
    deliveredto = models.TextField(blank=True, null=True)
    datepaid = models.DateTimeField(blank=True, null=True)
    filluser = models.ForeignKey(User, related_name="requestsfilled")

    class Meta:
        permissions = (("can_view_requests", "View others' requests."),)

    def __unicode__(self):
        return u"User: %s Corp: %s" % (self.originuser.username, self.corprequest)


class RequestItem(models.Model):
    request = models.ForeignKey(Request, related_name="items")
    item = models.ForeignKey(Type, related_name="request_entries")
    qty = models.IntegerField()
    unitcost = models.BigIntegerField()

    def __unicode__(self):
        return u"Item: %s  Qty:  %s  Unit Cost:  %s" % (self.item.name, self.qty,
                self.unitcost)
