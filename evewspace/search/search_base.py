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
"""
This module provides the base search class.
"""
from django.db.models import Q
import json

__all__ = ('Searchbase',)

class SearchBase(object):

    def __init__(self, request):
        self.request = request

    limit_choices = 20
    choices = None
    search_fields = None

    def choice_value(self, choice):
        return choice.pk

    def choice_label(self, choice):
        return unicode(choice)

    def order_choices(self, choices):
        order_by = getattr(self, 'order_by', None)
        if order_by:
            return choices.order_by(order_by)
        return choices

    def choices_for_values(self):
        assert self.choices is not None, 'choices should be a queryset'
        return self.order_choices(self.choices.filter(pk__in=self.values or [])
                )[0:self.limit_choices]

    def choices_for_request(self):
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_field, 'search_field must be set'
        q = self.request.GET.get('term', '')

        conditions = Q()
        if q:
            conditions = Q(**{self.search_field.name + '__icontains': q})

        return self.order_choices(self.choices.filter(
            conditions))[0:self.limit_choices]

    def result_json(self):
        result = []
        for res in self.choices_for_request():
            result.append(unicode(res))
        return json.dumps(result)

