#!/bin/bash

curl -O https://www.fuzzwork.co.uk/dump/mysql56-odyssey-1.1-91288.tar.bz2
tar -xjvf /vagrant/puppet/scripts/mysql56-odyssey-1.1-91288.tar.bz2
mysql -u root -D djangotest < /vagrant/puppet/scripts/odyssey-1.1-91288/mysql56-odyssey-1.1-91288.sql
rm -rf /vagrant/puppet/scripts/odyssey-1.0-89097
/vagrant/evewspace/manage.py syncdb --noinput
/vagrant/evewspace/manage.py migrate
/vagrant/evewspace/manage.py buildsystemdata
/vagrant/evewspace/manage.py loaddata /vagrant/evewspace/*/fixtures/*.json
/vagrant/evewspace/manage.py defaultsettings
/vagrant/evewspace/manage.py resetadmin
/vagrant/evewspace/manage.py syncrss
