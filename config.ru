dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "lib")
$:.unshift File.join(dir, "..")

require "vc-server.rb"

run VC::Server
