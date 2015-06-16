README OSP
==========

The OSP website uses the Visual Culture api as basis to show our work based on our gitted practice. 
The osp app, contained in the visualculture project, can also be used as a standalone django app. This means
you don’t need to install all of visual culture locally when you just want to
work on the OSP website.

Getting started
---------------

# install django and additional django apps
# you can also use your distributions package manager,
# or create a virtual env

pip install "django<1.5" "django_compressor<1.5" "django-cors<0.2"

# to install the less css compiler, you need to install
# node js. download the latest version, and do a
# ./configure; make; sudo make install

# install the less compiler through npm:

sudo npm install -g less

# move into your osp folder, then get the files:

git clone git@git.constantvzw.org:osp.tools.visualculture.git
cd osp.tools.visualculture/visualculture/osp/

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

 /visualculture/osp            application
 /visualculture/osp/static     less, js, static images
 /visualculture/osp/templates  templates

