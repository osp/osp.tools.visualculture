# encoding: UTF-8
require 'grit'
require 'linguist'
require 'json'
require 'RMagick'
require 'rdiscount'

require 'sinatra/base'
require 'sinatra/reloader'

require 'vc-cache'
require 'vc-server'
require 'vc-transduction'
require 'vc-repo'
require 'vc-grit'

module VC
  settings = IO.read("#{File.dirname(__FILE__)}/../settings.json")
  @settings = JSON.parse(settings)
  @settings["image-sizes"] = [ @settings["preview-image-size"].to_i, @settings["thumb-image-size"].to_i ]

  def self.settings(setting=nil)
    if setting
      @settings[setting] #if defined? setting 
    else
      @settings.to_s
    end
  end
  
  def self.set(setting, args)
    @settings[setting] = args
  end
  
end
