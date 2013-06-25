Setting Up a Vagrant Development Environment
--------------------------------------------

A common question for those wishing to hack on Eve W-Space is "How do I quickly set up a test server on $OPERATING_SYSTEM?"

Eve W-Space provides a Vagrantfile and associated puppet manifests to quiclkly create standardized testing environments based on Ubuntu 12.04 LTS while still allowing you to work with your favorite coding tools.

Installing Vagrant and VirtualBox on Windows
............................................

First, you will need to have Oracle VirtualBox installed since Vagrant uses it to run VMs.

To install VirtualBox, download the installer form https://www.virtualbox.org/wiki/Downloads and install it.

Vagrant may be downloaded from http://downloads.vagrantup.com/ as an MSI installer package. Once installed, you may be asked to reboot.


Installing Vagrant and VirtualBox on GNU / Linux
................................................

This will vary based on your distribution. Many already have VirtualBox and Vagrant packaged in their package manager of choice, so check there first.

Vagrant can be downloaded as a Debian or RPM package from http://downloads.vagrantup.com/ or installed via Ruby Gems using :command: `$ gem install vagrant`.

VirtualBox is also packaged with many distributions, or can be downloaded in many binary formats at https://www.virtualbox.org/wiki/Linux_Downloads. You should also use dkms if offered to easily upgrade the VirtualBox kernel modules when you upgrade your kernel.


Creating an Eve W-Space Vagrant VM
..................................

Like any Vagrant-enabled applicaiton, the steps to run a test environment begin with (\*nix shown, but the same commands should work in Windows):

:command:`$ cd /path/to/code`

:command:`$ vagrant up`

At this point, Vagrant will download the base VM from the internet and start it up. Then it will automatically provision the Eve W-Space database and requirements via Puppet. It will not install a web server like Nginx or Apache since it is presumed you will use Django's test server for development.

Once provisioning is complete, you will need to access the VM via SSH by connecting to localhost on port 2222 (which is forwarded to the VM's port 22). 

On \*nix Vagrant provides a shortcut:

:command:`$ vagrant ssh`

On Windows, you will need to use the SSH client of your choice, such as PuTTY (http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

How you connect will depend on your client, but the information is:

* Host:     localhost (or 127.0.0.1)
* User:     vagrant
* Password: vagrant

Once you have connected ot the VM, you can administer it as you would any other server running Ubuntu 12.04 LTS. Your working directory will be mounted on the VM as */vagrant* To simply start the test server, run:

:command:`$ cd /vagrant/evewspace`

:command:`$ ./manage.py runserver 0.0.0.0:8000`

Now you should be able to connect to your test server in a web browser on your host at http://localhost:8080 .

You may also want to run Celery to handle background tasks. Open a second ssh shell and run:

:command:`$ /vagrant/evewspace/manage.py celery worker -B --loglevel=info`

Debugging output from background tasks will appear in this shell.


Developing with the Vagrant Test Environment
............................................

Since any changes to your working directory appear in the vagrant VM, simply use your favorite editor or IDE as you normally would. You may need to restart the Django test server if you cause a crash.

Please remember to only commit Unix style line endings or configure your git client to automatically convert on push.
