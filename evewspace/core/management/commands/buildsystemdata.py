from django.core.management.base import NoArgsCommand, CommandError
from core.models import *
from Map.models import *
from Map.utils import RouteFinder
import datetime
import pytz

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        self.stdout.write('Beginning System Table Construction')
        basedata = SystemData.objects.all()
        for system in basedata:
            #self.stdout.write('Processing system: %s' % (system.name))
            try:
                sysclass = LocationWormholeClass.objects.get(location=system.region.id).sysclass
                if sysclass > 6:
                    newdata = KSystem(sov='', sysclass=sysclass, 
                            lastscanned=datetime.datetime.utcnow().replace(tzinfo=pytz.utc), 
                            info='', occupied='')
                    for field in system._meta.fields:
                        setattr(newdata, field.attname, getattr(system, field.attname))
                    newdata.systemdata_ptr = system
                    newdata.jumps = 0
                    newdata.podkills = 0
                    newdata.npckills = 0
                    newdata.shipkills = 0
                    newdata.save()
                else:
                    # TODO: Populate statics by constellation
                    newdata = WSystem(static1=None, static2=None, sysclass=sysclass, 
                            lastscanned=datetime.datetime.utcnow().replace(tzinfo=pytz.utc), 
                            info='', occupied='')
                    for field in system._meta.fields:
                        setattr(newdata, field.attname, getattr(system, field.attname))
                    newdata.systemdata_ptr = system
                    newdata.podkills = 0
                    newdata.npckills = 0
                    newdata.shipkills = 0
                    newdata.save()
            except LocationWormholeClass.DoesNotExist:
                pass
            except DoesNotExist:
                self.stderr.write('Unable to process %s' % (system.name))
        self.stdout.write('First Pass Complete, beginning lowsec pass')
        for system in basedata:
            try:
                sysclass = LocationWormholeClass.objects.get(location = system.id).sysclass
                lowsec = KSystem.objects.get(name=system.name)
                lowsec.sysclass = sysclass
                lowsec.save()
            except LocationWormholeClass.DoesNotExist:
                pass
        # Get a quick route to build the SystemJump cache
        sys1 = KSystem.objects.get(name="Jita")
        sys2 = KSystem.objects.get(name="Amarr")
        RouteFinder(sys1, sys2).route_length()
