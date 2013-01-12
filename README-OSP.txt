README OSP
==========

The OSP website uses the Visual Culture api as basis. The osp app, contained
in the vc_django project, can also be used as a standalone django app. This means
you don’t need to install all of visual culture locally when you just want to
work on the OSP website.

Getting started
---------------

# install django and additional django apps
# you can also use your distributions package manager,
# or create a virtual env

sudo pip install django django_compressor

# to install the less css compiler, you need to install
# node js. download the latest version, and do a
# ./configure; make; sudo make install

# install the less compiler through npm:

sudo npm install -g less

# move into your osp folder, then get the files:

git clone git@git.constantvzw.org:osp.tools.visualculture.git
cd osp.tools.visualculture/vc_django/osp/

# create settings file

cp settings.py.example settings.py

# run development server

python manage.py runserver

# now you can make changes and check your progress on the development
# server. When you are happy, commit. To propagate your changes to the
# server, run:

make


Directory layout
----------------

 /public                   less, js, static images
 /vc_django/osp            application
 /vc_django/osp/templates  templates

