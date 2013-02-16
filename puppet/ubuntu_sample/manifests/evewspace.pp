class evewspace {
	include git
	include supervisor

	group { 'evewspace':
		ensure => present,
	}

	user { 'evewspace':
		ensure => present,
		home => '/home/evewspace',
		gid => 'evewspace',
		managehome => 'true',
		password => 'reallysecretpassword',
		require => Group['evewspace']
	}

	package {'build-essential':
		ensure => present,
	}

	package {'libmysqlclient-dev':
		ensure => present,
	}

	package {'python-dev':
		ensure => present,
	}

	package {'mysql-client':
		ensure => present,
	}

	package {'python-pip':
		ensure => present
	}

	package {'git-core':
		ensure => present,
	}

	package {'bzip2':
		ensure => present,
	}

	package {'nginx':
		ensure => present,
	}

	package {'mysql-server':
		ensure => present,
	}

	package {'memcached':
		ensure => present,
	}

	package {'rabbitmq-server':
		ensure => present,
	}

	service {'rabbitmq-server':
		ensure => 'running',
		hasrestart => 'true',
		hasstatus => 'true',
		require => Package['rabbitmq-server']
	}

	service {'mysql':
		ensure => 'running',
		provider => 'upstart',
		hasrestart => 'true',
		hasstatus => 'true',
		require => Package['mysql-server']
	}

	service {'nginx':
		ensure => 'running',
		hasrestart => 'true',
		hasstatus => 'true',
		require => Package['nginx']
	}

    # Copy nginx site config from a puppet template (to get the hostname right)
	file { '/etc/nginx/sites-available/evewspace':
		ensure => file,
		content => template('nginx-site.conf'),
		require => Package['nginx']
	}

	file {'/etc/nginx/sites-enabled/default':
		ensure => absent,
		require => Package['nginx']
	}

	file {'/etc/nginx/sites-available/default':
		ensure => absent,
		require => Package['nginx']
	}

	file {'/etc/nginx/sites-enabled/evewspace':
		ensure => link,
		target => '/etc/nginx/sites-available/evewspace',
		require => File['/etc/nginx/sites-available/evewspace']
	}

    # Grab the latest code
	git::repo {'evewspace':
		path => '/home/evewspace/evewspace',
		source => 'https://github.com/marbindrakon/eve-wspace.git',
		branch => 'master',
		update => 'false',
		require => User['evewspace'
	}

    # Create our local_settings.py file to override defaults stored in git
	file { '/home/evewspace/evewspace/evewspace/evewspace/local_settings.py':
		ensure => present,
		source => 'puppet:///files/local_settings.py',
		require => git::repo['evewspace'],
	}

    # Install the dependencies
	exec { 'easy_install':
		command => 'easy_install -U distribute',
		require => Package['python-pip']
	}

	exec { 'requirements':
		cwd => '/home/evewspace/evewspace',
		command => 'pip install -r requirements.txt',
		timeout => 0,
		require => [Service['mysql'], Package['libmysqlclient-dev'], Package['python-dev'], Package['python-pip'], git::repo['evewspace'], Exec['easy_install'], Package['python-dev']]
	}

    # Copy a mysql version of the SDE from the puppet fileserver.
	file { '/home/evewspace/staticdata.sql':
		ensure => present,
		source => 'puppet:///files/staticdata.sql',
		require => User['evewspace']
	}

    # Grab a script from the file server to initialize the database and run it if the database doesn't exist
	file { '/home/evewspace/load_db.sh':
		ensure => present,
		source => 'puppet:///files/load_db.sh',
		mode => 0774,
		require => git::repo['evewspace']	
	}

    exec { 'loaddb':
		cwd => '/home/evewspace',
		timeout => 0,
		unless => '/usr/bin/mysql -uroot  evewspace',
		command => '/home/evewspace/load_db.sh',
		require => File['/home/evewspace/load_db.sh']
	}

    # Collect the static files so Nginx can serve them
	exec { 'collectstatic':
		command => 'python /home/evewspace/evewspace/evewspace/manage.py collectstatic --noinput',
		require => Exec['requirements']
	}

    # Install gunicorn to serve the django application (Nginx will proxy)
	exec { 'gunicorninstall':
		command => 'pip install gunicorn',
		require => Exec['requirements']
	}

    # Have supervisor run celery and gunicorn for us
	supervisor::service { 'celeryd':
		ensure => present,
		command => '/usr/bin/python /home/evewspace/evewspace/evewspace/manage.py celery worker -B --loglevel=INFO --concurrency=3',
		directory => '/home/evewspace/evewspace',
		user => 'evewspace',
		group => 'evewspace',
		require => Exec['setperms']
	}

	supervisor::service { 'gunicorn':
		ensure => present,
		command => 'gunicorn_django -w 4 /home/evewspace/evewspace/evewspace/evewspace/settings.py',
		user => 'evewspace',
		group => 'evewspace',
		require => Exec['setperms']
	}

    # Puppet's git module likes to own everything to root, fix that.
	exec { 'setperms':
		command => 'chown -R evewspace:evewspace /home/evewspace',
		require => Exec['loaddb']
	}
}
	
