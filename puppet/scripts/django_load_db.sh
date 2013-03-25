!#/bin/bash

wget http://donbot.fcftw.org/mysql55-inferno12-extended.sql.bz2
bunzip2 /home/vagrant/mysql55-inferno12-extended.sql.bz2
mysql -u root -D djangotest < /home/vagrant/mysql55-inferno12-extended.sql
rm /home/vagrant/mysql55-inferno12-extended.sql
/vagrant/evewspace/manage.py syncdb --noinput
/vagrant/evewspace/manage.py migrate
/vagrant/evewspace/manage.py buildsystemdata
/vagrant/evewspace/manage.py loaddata /vagrant/evewspace/*/fixtures/*.json
/vagrant/evewspace/manage.py defaultsettings
/vagrant/evewspace/manage.py resetadmin
/vagrant/evewspace/manage.py syncrss
