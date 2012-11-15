from search import registry
from models import Type

registry.register(Type, 'item', 'name', 
        Type.objects.filter(published=True).all())
