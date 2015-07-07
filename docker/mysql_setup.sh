#!/bin/bash
/usr/sbin/mysqld &
sleep 10
echo "CREATE DATABASE evewspace CHARACTER SET utf8;" | mysql
echo "GRANT ALL PRIVILEGES ON evewspace.* TO '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASS}';" | mysql
