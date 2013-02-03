from search import registry
from models import Type

registry.register(Type, 'item', 'name',
        Type.objects.filter(published=1).all())
registry.register(Type, 'tower', 'name',
        Type.objects.filter(published=1, marketgroup__pk=478).all())
