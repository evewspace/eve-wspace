from search import registry
from models import Corporation, Alliance

registry.register(Corporation, 'corp', 'name')
registry.register(Alliance, 'alliance', 'name')
