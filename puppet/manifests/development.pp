group {'puppet':
	ensure => present,
	}

package {'build-essential':
	ensure => present,
	}

package {'python-pip':
	ensure => latest,
	require => Exec['apt-get update'],
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

package {'git-core':
	ensure => present,
	}

package {'bzip2':
	ensure => present
	}

package {'mysql-server':
	ensure => present,
	}

package {'memcached':
    ensure => present,
    }

service {'mysql':
	ensure => 'running',
	provider => 'upstart',
	hasrestart => 'true',
	hasstatus => 'true',
	require => Package['mysql-server']
	}

exec {'easy_install -U distribute':
	command => "/usr/bin/easy_install -U distribute",
	require => Package['python-pip'],
	}

exec {'apt-get update':
	command => "/usr/bin/apt-get update"
	}

exec {'create-db':
        unless => "/usr/bin/mysql -uroot  djangotest",
	cwd => "/home/vagrant",
        command => "/usr/bin/mysql -e \"create database djangotest;\" && /vagrant/puppet/scripts/django_load_db.sh",
	timeout => 0,
        require => [ Service["mysql"], Package['mysql-server'], Exec['requirements'], Package['bzip2'], Package['memcached'] ]
	}

exec {'requirements':
	command => "/usr/bin/pip install -r /vagrant/requirements.txt",
	timeout => 0,
	require => [Package["python-pip"], Exec['easy_install -U distribute'], Package['libmysqlclient-dev'], Package['python-dev'] ],
	}
