OSP Visual Culture Git Viewer
=============================

- - -

$ sudo gem install sinatra grit haml shotgun bundler


Linguist-specific install
========================

$ cd /tmp
$ git clone https://github.com/github/linguist.git
$ cd linguist/
$ cp #{osp.tools.visualculture}/patches/mimes.yml lib/linguist/
$ cp #{osp.tools.visualculture}/patches/test_mime.rb test/
$ bundle install
$ gem build linguist.gemspec
$ sudo gem install linguist-1.0.0.gem

Using
=====

Use shotgun to serve with auto reload,
specify git repo as argument

From the folder osp.tools.visualculture:

$ shotgun app.rb "/home/e/osp/osp.work.panik"

Troubleshooting
===============

- If you run into any errors relating to 'lib.so' missing, the solution is to edit `/usr/lib/ruby/gems/1.9.1/gems/rubypython-0.5.3/lib/rubypython/pythonexec.rb`. Find where @library is assigned and set it manually rather than relying on the `find_python_lib` method. On ArchLinux, this means `@library = "/usr/lib/libpython2.7.so`. You can also set `@python = "python2"` to remove any further doubts.

- If you receive an error about "missing magic files", re-install charlock_holmes gem: `gem install charlock_holmes -- --with-icu-dir=/usr/share/icu/4.8.1.1/` (again, the directory in the example is from ArchLinux).

- You need to (re)build the linguist gem as above to add the new mimetypes. At least, on ArchLinux simply copying the files directly into the `/usr/lib/ruby/gem` tree at their respective locations did not work, but re-building and re-installing did.
