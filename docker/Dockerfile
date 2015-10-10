# EVE WSPACE MYSQL
#
# VERSION               0.2

FROM ubuntu:12.04
MAINTAINER Papazafeiropoulos Giorgos <g.papazafeiropoulos@gmail.com>

# Exposed ENV
#Modify them to depict your instalation environment
#NGINX server name
ENV NGINX_HOSTNAME rens
#MYSQL user and password for the application
ENV MYSQL_USER maptool
ENV MYSQL_PASS maptool123
#DJANGO unique key - create a new one!
ENV DJANGO_KEY @o3zk1@4^d3osu-om9-_=(hvr48o*%c+@h3d$%pg2g+ta2g2v(


# DO NOT MODIFY THESE!
# avoid debconf and initrd
ENV DEBIAN_FRONTEND noninteractive
ENV INITRD No


#Update packages and install needed.
RUN apt-get -y update
RUN apt-get install -y git-core build-essential python-dev python-pip nginx bzip2 memcached libmysqlclient-dev mysql-server libxml2-dev libxslt-dev rabbitmq-server supervisor curl sudo libyaml-dev vim
RUN	sed	-i -e "s/^bind-address\s*=\s*127.0.0.1/bind-address	=	0.0.0.0/"	/etc/mysql/my.cnf

#Set up nginx as daemon off.
RUN sed -i -e '1idaemon off;' /etc/nginx/nginx.conf

RUN easy_install -U distribute 
RUN pip install virtualenv

#Set up the mysql db.
ADD mysql_setup.sh /mysql_setup.sh
RUN chmod +x /mysql_setup.sh
RUN /mysql_setup.sh

# set root password
RUN echo "root:root" | chpasswd

# copy supervisor conf
ADD supervisor/conf.d /etc/supervisor/conf.d

ADD evewspace.sh evewspace.sh
RUN chmod +x evewspace.sh

#Set Maptool user
RUN adduser --disabled-password --gecos '' ${MYSQL_USER} && adduser ${MYSQL_USER} sudo && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ${MYSQL_USER}
WORKDIR /home/${MYSQL_USER}
RUN mkdir /home/${MYSQL_USER}/static

#Get eve-wspace code
RUN git clone https://github.com/marbindrakon/eve-wspace.git


#Install the eve dumb data
RUN curl -O https://www.fuzzwork.co.uk/dump/mysql-latest.tar.bz2
RUN mkdir evedumb && tar xvf mysql-latest.tar.bz2 -C evedumb

RUN sudo /usr/sbin/mysqld &\
	sleep 10s &&\
	sudo find ./evedumb -type f -name "*.sql" -exec sh -c "mysql -u ${MYSQL_USER} -p${MYSQL_PASS} evewspace < {}" \;

RUN rm -rf evedumb
RUN rm -rf mysql-latest.tar.bz2

#Install Eve-Wspace Environment
#Add evewspace configuration tool and make it accessible
RUN sudo /usr/sbin/mysqld &\
	sleep 10s &&\ 
	/evewspace.sh

#Get back to root
USER root

#Set up nginx
ADD nginx/evewspace /etc/nginx/sites-available/evewspace
RUN sed -i -e "s/server_name name;/server_name ${NGINX_HOSTNAME};/"	/etc/nginx/sites-available/evewspace
RUN sed -i -e "s/{MYSQL_USER}/${MYSQL_USER}/" /etc/nginx/sites-available/evewspace
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/evewspace /etc/nginx/sites-enabled/evewspace

#Set up celery and gunicorn
RUN sed -i -e "s/{MYSQL_USER}/${MYSQL_USER}/g" /etc/supervisor/conf.d/celery.conf
RUN sed -i -e "s/{MYSQL_USER}/${MYSQL_USER}/g" /etc/supervisor/conf.d/gunicorn.conf
# clean packages
RUN apt-get clean
RUN rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# start supervisor
EXPOSE 80
CMD ["/usr/bin/supervisord"]
