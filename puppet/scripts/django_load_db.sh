#!/bin/bash

curl -O https://www.fuzzwork.co.uk/dump/mysql-latest.tar.bz2
tar -xjvf /vagrant/puppet/scripts/mysql-latest.tar.bz2
mysql -u root -D djangotest < /vagrant/puppet/scripts/*/*.sql
rm -rf /vagrant/puppet/scripts/*-*
/vagrant/evewspace/manage.py syncdb --all --noinput
/vagrant/evewspace/manage.py migrate --fake
/vagrant/evewspace/manage.py buildsystemdata
/vagrant/evewspace/manage.py loaddata /vagrant/evewspace/*/fixtures/*.json
/vagrant/evewspace/manage.py defaultsettings
/vagrant/evewspace/manage.py resetadmin
/vagrant/evewspace/manage.py syncrss
