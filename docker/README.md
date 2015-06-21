Docker Set Up
=============

What is it?
-----------
A docker container that can be used to quickly provision a functional eve-wspace application stack.
Will pull latest code from github, latest packages for dependencies for Ubuntu 12.04 LTS, and latest 
evedumb database and create an image with all these installed and configured to run the eve-wspace application.
Will set it up to use mysql db and nginx as described in the documentation for installing the application.
Supervisor is used to make sure everything is started and run as expected.

Documentation
-------------

Prerequisites
-------------
A running installation of Docker is required. Version used is 1.5.0, so use that or later.
Basic knowledge of Docker commands and how all work will be beneficial.

Create the image
----------------
Docker containers are based on an image. We will create an image that will have the eve-wspace 
ready servicing users. Thus all configurations shall be done at this step. This will allow faster 
start up times since we won't have to initialize db's ect. 

Clone/Download the project and cd into the docker directory. The Dockerfile must be in your current directory.
Open it with a text editor and edit the environment variables at the top of the file, to your liking.

Create the image named gpapaz/eve-wspace-mysql.

	$ sudo docker build -t "gpapaz/eve-wspace-mysql" .

Wait till you see the end of the process ... and a success message!
You can check that the image was build with:

	$ sudo docker images | grep "gpapaz/eve-wspace-mysql"

If you want to remove the created image - thus not been able to start new evewspace containers -
just type:

	$ sudo docker rmi "gpapaz/eve-wspace-mysql"

Start a container
-----------------
Now that we have an image for our container we can start one or even more!

	$ sudo docker run -d -p 8080:80 --name evewspace gpapaz/eve-wspace-mysql

A new container named evewspace will be created, will be set to run as daemon, will 
redirect its internal 80 tcp port to our localhost's 8080 tcp port, and of course will 
be based to our eve-wspace image. When it is started the container will also start all the 
needed servers for the eve-wspace to operate as expected!

That's it! Your eve-wspace application is up and running and can be accessed from your PC through a 
web browser. Just point to 

	http::/<your_pc_ip>:8080 

or wherever your nginx server was configured during the image 
creation.

If you wish to stop the container:

	$ sudo docker stop evewspace

And to restart it:

	$ sudo docker start evewspace	

To access it while running:

	$ sudo docker exec -it evewspace /bin/bash

Use CTR-D or exit to return to your localhost.

And finally if you want to remove the container (stop it before):

	$ sudo docker rm evewspace

