#dir = File.dirname(__FILE__)
#$:.unshift(File.join(dir, ".."))
%w(sinatra grit linguist json RMagick).each { |gem| require gem }

require 'vc-transduction'
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
  
end
