OSP Visual Culture Git Viewer
=============================

We are Open Source Publishing. A group of designers working in Brussels. We make books and posters and websites, and we do that using only Free and Open Source Software. That is because we feel it is important to have an intimate relation with our tools. If all designers use the same tools made by the same company, this is bound to make us less creative and less relevant.

For working together and sharing our source files, we use a system called Git. This system, originally developed for computer code, is great to work together. Yet when we started sharing our source code through the internet, we found all interfaces to git were geared to sharing text files. We want to create an interface for sharing our work

We have been displaying the contents of our repository in a more graphic way: showing previews in the filelistings of the fonts and the illustrations and the pdf’s. We want to take this a whole step further still, and build this into a platform where you can in a visual way view the development of your graphic design projects, the changes in between files, and comment and share and make visible your process.

- - -

Installation
============

Get the code
------------

$ git clone git://git.constantvzw.org/osp.tools.visualculture.git

Prerequisites
-------------

(Note that grit/shotgun/bundler/commander aren't packaged on Debian)

$ sudo gem install sinatra sinatra-contrib grit shotgun bundler json rmagick commander

When running ruby 1.8, in addition:

$ sudo gem install minitest


Linguist-specific install
-------------------------

$ cd /tmp # please! :)
$ git clone https://github.com/ab5tract/linguist.git
$ cd linguist/
$ sudo bundle install
$ gem build linguist.gemspec
$ sudo gem install linguist-1.0.0.gem

Using
=====

This gem ships with a command-line program, 'visualculture'.

This command allows you to start the Visual Culture web application in three ways:

1) By passing a list of repositories as an argument:
      $ visualculture server "thisgit" "project/thatgit" "an/othergit"
2) By running in a directory containing git repositories:
      $ visualculture server
3)  By running in a directory that itself contains a repository:
      $ visualculture server
      
The last two options use the same command but respond differently depending if run from within a git repository or not.

Troubleshooting
===============

- On Ubuntu, with Ruby 1.8 you can get errors like:
Invalid gemspec in [/path/to/gemspec/tilt-1.3.3.gemspec]: invalid date format in specification: "2011-08-25 00:00:00.000000000Z"
You need to update gem, as such:

$ sudo gem install rubygems-update
$ sudo update_rubygems

- On Ubuntu, building the rmagick gem requires you to first "sudo apt-get install libmagick9-dev"

- On Ubuntu, building the Charlock Holmes gem requires you to first "sudo apt-get install libicu-dev", on Fedora "yum install libicu-devel"" 

*Archlinux:*

- If you run into any errors relating to 'lib.so' missing, the solution is to edit `/usr/lib/ruby/gems/1.9.1/gems/rubypython-0.5.3/lib/rubypython/pythonexec.rb`. Find where @library is assigned and set it manually rather than relying on the `find_python_lib` method. On ArchLinux, this means `@library = "/usr/lib/libpython2.7.so`. You can also set `@python = "python2"` to remove any further doubts.

- If you receive an error about "missing magic files", re-install charlock_holmes gem: `gem install charlock_holmes -- --with-icu-dir=/usr/share/icu/4.8.1.1/` (again, the directory in the example is from ArchLinux).

- You need to (re)build the linguist gem as above to add the new mimetypes. At least, on ArchLinux simply copying the files directly into the `/usr/lib/ruby/gem` tree at their respective locations did not work, but re-building and re-installing did.
