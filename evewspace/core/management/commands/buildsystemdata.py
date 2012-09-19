from django.core.management.base import NoArgsCommand, CommandError
from core.models import *
from Map.models import *
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
                    newdata.save()
                else:
                    # TODO: Populate statics by constellation
                    newdata = WSystem(static1=None, static2=None, sysclass=sysclass, 
                            lastscanned=datetime.datetime.utcnow().replace(tzinfo=pytz.utc), 
                            info='', occupied='')
                    for field in system._meta.fields:
                        setattr(newdata, field.attname, getattr(system, field.attname))
                    newdata.systemdata_ptr = system
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
