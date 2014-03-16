Eve W-Space v0.2.2
===========

NOTE: Eve W-Space is currently in alpha. Most features outside of Mapping 
are not yet implemented past some prototype data models. 

What is it?
-----------
Eve W-Space is, at its core, a wormhole mapping and intel tool for the MMORPG 
Eve Online. If you wish, it can be much more. It can be customized to fill 
roles from simple mapping applicaiton (with all extra features disabled) to 
the centerpiece of an entire alliance services infrastructure.

Eve W-Space is designed to be a single-tenant soulution hosted by a single corp 
or alliance. A fleixble permissions system allows for easily restricting data 
where needed.

Documentation
-------------

Documentation is available at http://eve-w-space.rtfd.org

How do I use it?
----------------
Generally, Eve W-Space requires:

* Django 1.6+
* Python 2.6-2.7
* Celery
* RabbitMQ (preferred)
* memcached (preferred)
* An RDBMS (MariaDB, MySQL, and PostgreSQL tested)

Other required python modules are listed in requirements.txt.

How Eve W-Space is installed will depend on the environment, a sample Puppet 
manifest (based on Ubuntu 12.04 LTS, Nginx, and Gunicorn) and scripts are 
provided in the puppet/sample directory to get you started while proper 
documentation is lacking.

For quick testing and hacking, a Vagrantfile is provided to get up and running 
quickly, the manifest used by the Vagrant VM does not automatically install a web 
server.


