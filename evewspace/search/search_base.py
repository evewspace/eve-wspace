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
        q = self.request.GET.get('q', '')

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

