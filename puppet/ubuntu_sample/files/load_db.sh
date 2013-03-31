#!/bin/bash
mysql -u root -e "create database evewspace character set utf8;"
mysql -u root -D evewspace < /home/evewspace/staticdata.sql
/home/evewspace/evewspace/evewspace/manage.py syncdb --noinput
/home/evewspace/evewspace/evewspace/manage.py migrate
/home/evewspace/evewspace/evewspace/manage.py buildsystemdata
/home/evewspace/evewspace/evewspace/manage.py loaddata /home/evewspace/evewspace/evewspace/*/fixtures/*.json
/home/evewspace/evewspace/evewspace/manage.py defaultsettings
/home/evewspace/evewspace/evewspace/manage.py resetadmin
/home/evewspace/evewspace/evewspace/manage.py syncrss
