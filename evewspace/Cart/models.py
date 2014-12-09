#   Eve W-Space
#   Copyright 2014 Andrew Austin and contributors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from django.db import models
from django.conf import settings
from core.models import Type

# Create your models here.

User = settings.AUTH_USER_MODEL

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
