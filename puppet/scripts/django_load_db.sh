#!/bin/bash

curl -O http://www.fuzzwork.co.uk/dump/mysql55-odyssey-1.0-89097.tbz2
tar xvjf /vagrant/puppet/scripts/mysql55-odyssey-1.0-89097.tbz2
mysql -u root -D djangotest < /vagrant/puppet/scripts/odyssey-1.0-89097/mysql55-odyssey-1.0-89097.dmp
rm -rf /vagrant/puppet/scripts/odyssey-1.0-89097
/vagrant/evewspace/manage.py syncdb --noinput
/vagrant/evewspace/manage.py migrate
/vagrant/evewspace/manage.py buildsystemdata
/vagrant/evewspace/manage.py loaddata /vagrant/evewspace/*/fixtures/*.json
/vagrant/evewspace/manage.py defaultsettings
/vagrant/evewspace/manage.py resetadmin
/vagrant/evewspace/manage.py syncrss
