VISUAL CULTURE GIT VIEWER
=========================

* Note: there will be a simpler version of this procedure,
  to install just the OSP website for development. A large
  part of this machinery can stay online on the Constant
  server. *

Installation
------------

### OS Dependencies

#### Debian / Ubuntu

sudo apt-get install rabbitmq-server

Get the latest libgit2 release from https://github.com/libgit2/libgit2/downloads
and build it as in the instructions provided on http://libgit2.github.com.

Finally Python can’t automatically find the libraries, you have to tell it
where they are at, do:

sudo ldconfig

#### OS X

brew install libmagic libgit2

### Python modules

Run-of-the-mill python modules required:

django
python-magic
django-celery
pygit2 (built from source or via pip)

### Setting up django

cp settings_example.py settings.py

In the settings file, you will at least need to change the `GIT_ROOT` setting.
This is the folder that Visual Culture will scan for git repositories.

then run `python manage.py syncdb`

You can then use `python manage.py runserver` to run the application

You have to run the Celery queue at the same time if you want to use
Visual Culture’s image generation functions. For that you first need to
set up RabbitMQ:

### Setting up rabbitmq

sudo rabbitmqctl add_user user password
sudo rabbitmqctl set_permissions user '.*' '.*' '.*'

### Setting up the Celery queue

Run the queue as:

python manage.py celeryd --purge -E -c 2

This means that in development you’ll have two development servers
running: the Celery queue en the Django server.

Adding vc image rendering components
------------------------------------

### PDF-SUPPORT : Poppler

#### Ubuntu:

sudo apt-get install libpoppler-cpp-dev libpoppler-qt4-dev libboost-dev libboost-python-dev libboost-system-dev libboost-thread-dev

#### Debian

well, just a note

a) remove the leading 'lib' from the resulting library filename
b) drop it wherever Python can find it and it will be available as a module
c) because the Debian we run on doesn't have libpoppler-cpp, I got the 0.20 tarball, compile it and installed it in the venv we use for this deployment, then adjusted PKG_CONFIG_PATH to make cmake find it


#### Then:

mkdir build && cd build
cmake ..
make
ln -s libvc_poppler.so ../../vc_django/visual_culture/readers/vc_poppler.so

#### OSX

brew install poppler boost

### FONT-SUPPORT

sudo apt-get install python-fontforge fontforge

#### OSX

brew install fontforge

Maintenance
-----------

### Empty the cache

rm -rf {MEDIAROOT}/cache
python manage.py reset vc_cache
