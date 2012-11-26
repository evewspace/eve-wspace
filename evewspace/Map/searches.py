from search import registry
from models import System, WormholeType, SiteSpawn

registry.register(System, 'system', 'name')
registry.register(WormholeType, 'whtype', 'name')
registry.register(SiteSpawn, 'site','sitename') 
