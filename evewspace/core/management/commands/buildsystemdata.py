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
            # Prevent trying to add duplicate systems if run on an existing DB
            if System.objects.filter(pk=system.pk).exists():
                continue
            try:
                sysclass = LocationWormholeClass.objects.get(location=system.region.id).sysclass
                if sysclass in range(7,12):
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
