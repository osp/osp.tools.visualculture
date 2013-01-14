well, just a note

a) remove the leading 'lib' from the resulting library filename
b) drop it wherever Python can find it and it will be available as a module
c) because the Debian we run on doesn't have libpoppler-cpp, I got the 0.20 tarball, compile it and installed it in the venv we use for this deployment, then adjusted PKG_CONFIG_PATH to make cmake find it
