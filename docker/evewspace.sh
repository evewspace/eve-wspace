#! /bin/bash
virtualenv --no-site-packages /home/maptool/eve-wspace 
source /home/maptool/eve-wspace/bin/activate 
pip install -r /home/maptool/eve-wspace/requirements-mysql.txt 

cd /home/maptool/eve-wspace/evewspace/evewspace 
cp local_settings.py.example local_settings.py 
sed -i -e "s/'alan_please_add_secret_key'/'${DJANGO_KEY}'/" local_settings.py
sed -i -e "s/'django.db.backends.'/'django.db.backends.mysql'/" local_settings.py 
sed -i -e "s/'root'/'${MYSQL_USER}'/" local_settings.py 
sed -i -e "s/'PASSWORD': ''/'PASSWORD': '${MYSQL_PASS}'/" local_settings.py 
sed -i -e "s/DEBUG = True/DEBUG = False/" local_settings.py

cd /home/maptool/eve-wspace/evewspace 
echo "./manage.py syncdb --all --noinput"
./manage.py syncdb --all --noinput 
echo "./manage.py migrate --fake"
./manage.py migrate --fake 
echo "./manage.py buildsystemdata"
./manage.py buildsystemdata 
echo "./manage.py loaddata */fixtures/*.json"
./manage.py loaddata */fixtures/*.json 
echo "./manage.py defaultsettings"
./manage.py defaultsettings 
echo "./manage.py resetadmin"
./manage.py resetadmin 
echo "./manage.py syncrss"
./manage.py syncrss 
echo "./manage.py collectstatic --noinput"
./manage.py collectstatic --noinput 

echo "Install gunicorn"
pip install gunicorn


