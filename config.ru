# encoding: UTF-8
dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "views")
$:.unshift File.join(dir, "lib")

require "vc-server.rb"
run VC::Server.new
