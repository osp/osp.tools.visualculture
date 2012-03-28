dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "lib")
$:.unshift File.join(dir, "..")

require "lib/vc-server.rb"

run VC::Server
