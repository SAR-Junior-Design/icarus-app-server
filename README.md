# icarus-app-server
This is the Application Server of the Icarus Drone management system.


## Setup

### Python

Python is currently v3.6, until 3.7 stabilizes a bit more.

### Postgres

Most of the data in our server is stored in postgres. This is how you can setup a postgres database with all of the bells and whistles we need.

First, download postgres:

`sudo apt-get install postgres`

Then enter the database via `psql postgres`.

`create user django_user`
grant 

### Geodjango

This application server uses Postgis to maintain geolocated data.

Therefore there's some shit you have to setup.

Read this link, one day I will have a more comprehensive tutorial on this readme: https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/