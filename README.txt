VISUAL CULTURE GIT VIEWER
=========================

OSP Visual Culture Git Viewer
=============================

We are Open Source Publishing. A group of designers working in Brussels. We make books and posters and websites, and we do that using only Free and Open Source Software. That is because we feel it is important to have an intimate relation with our tools. If all designers use the same tools made by the same company, this is bound to make us less creative and less relevant.

For working together and sharing our source files, we use a system called Git. This system, originally developed for computer code, is great to work together. Yet when we started sharing our source code through the internet, we found all interfaces to git were geared to sharing text files. We want to create an interface for sharing our work

We have been displaying the contents of our repository in a more graphic way: showing previews in the filelistings of the fonts and the illustrations and the pdf’s. We want to take this a whole step further still, and build this into a platform where you can in a visual way view the development of your graphic design projects, the changes in between files, and comment and share and make visible your process.

- - -

* Note: this is for installing the Visual Culture API
  for working on the OSP website, there is a more simple
  application that interfaces with the API.
  See README-OSP.txt *

Installation
------------

### OS Dependencies

#### Debian / Ubuntu

Libgit2 needs to be compiled from source:

    sudo apt-get install build-essential cmake
    mkdir -p ~/src
    cd ~/src
    curl https://github.com/downloads/libgit2/libgit2/libgit2-0.17.0.tar.gz | tar xvz
    cd libgit2-0.17.0
    mkdir build && cd build
    cmake ..
    cmake --build .
    sudo cmake --build . --target install
    sudo ldconfig

#### OS X

brew install libmagic libgit2

### Python modules

Run-of-the-mill python modules required:

- django
- python-magic
- pygit2 (built from source or via pip)

Django apps:

- django-cors

### Setting up django

From inside the `visualculture` folder:

    cp settings.py.example settings.py

In the settings file, you will at least need to change the `GIT_ROOT` setting.
This is the folder that Visual Culture will scan for git repositories.

then run

    python manage.py syncdb

You can then use `python manage.py runserver` to run the application


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
    ln -s libvc_poppler.so ../../visualculture/visual_culture/readers/vc_poppler.so

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
