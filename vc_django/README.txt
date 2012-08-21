VISUAL CULTURE GIT VIEWER
=========================

Installation
------------

Run-of-the-mill python modules required:

django
python-magic

To install pygit2, you need to first build libgit2

Careful! libgit2’s default branch is ‘development’
pygit2 is developed against ‘master’

after cloning libgit2, do:

git checkout --track origin/master

to checkout and switch to the master branch.

Then proceed to build libgit2 following the instructions
on its website.

Pygit2 install instructions are found on it’s website,
but I found quite recent versions are on pypi as well.

One final caveat:

Python expects to find installed libraries in the path
specified by the environment library LD_LIBRARY_PATH
if this is not specified you will get the error

ImportError: libgit2.so.0: cannot open shared object file: No such file or directory

In this case you can add for example

export LD_LIBRARY_PATH=/usr/local/lib

to your .bashrc,
see:  http://stackoverflow.com/questions/1099981/why-cant-python-find-shared-objects-that-are-in-directories-in-sys-path

