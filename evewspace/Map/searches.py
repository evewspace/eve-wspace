from search import registry
from models import System, WormholeType

registry.register(System, 'system', 'name')
registry.register(WormholeType, 'whtype', 'name')
