README OSP
==========

The OSP website uses the Visual Culture api as basis to show our work based on our gitted practice.
The osp app, contained in the visualculture project, can also be used as a standalone django app. This means
you don’t need to install all of visual culture locally when you just want to
work on the OSP website.

Getting started
---------------

- install django and additional django apps
- you can also use your distributions package manager,
- or create a virtual env

install dependencies via pip inside your virtual env, the OSP dependencies are gathered in a requirments.txt inside folder osp/

``pip install -r requirements.txt``

At the time of this writing, dependencies are so:

- Django==1.4.20
- Markdown==2.6.2
- amqp==1.4.6
- anyjson==0.3.3
- argparse==1.2.1
- billiard==3.3.0.20
- celery==3.1.18
- django-appconf==1.0.1
- django-celery==3.1.16
- django-compressor==1.4
- django-cors==0.1
- kombu==3.0.26
- pytz==2015.4
- six==1.9.0
- wsgiref==0.1.2

to install the less css compiler, you need to install node js. download the latest version, and do a

`./configure`
`make`
`sudo make install`

install the less compiler through npm:

``sudo npm install -g less``

move into your osp folder, then get the files:

``git clone git@git.constantvzw.org:osp.tools.visualculture.git``
``cd osp.tools.visualculture/visualculture/osp/``

create settings file

``cp settings.py.example settings.py``

run development server

``python manage.py runserver``

now you can make changes and check your progress on the development server. When you are happy, commit. To propagate your changes to the server, run:

``make``


Directory layout
---

 /visualculture/osp            `application`

 /visualculture/osp/static     `less, js, static images`

 /visualculture/osp/templates  `templates`
