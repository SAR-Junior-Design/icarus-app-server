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

## Run

You will need three different `screen` instances with the following commands typed in to run this server: 

First one is the django server: `python manage.py runserver`

Or to run through gunicorn: `gunicorn --bind 0.0.0.0:8000 myproject.wsgi:application`

Second one is the redis-server: `redis-server`

Third one is the celery worker: `celery worker -A icarus_backend --loglevel=debug --concurrency=1`

## Authentication

We use OAuth2 to authenticate users, though for superusers we also have the model backend. 