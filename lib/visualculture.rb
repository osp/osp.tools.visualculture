#dir = File.dirname(__FILE__)
#$:.unshift(File.join(dir, ".."))
%w(sinatra grit linguist json RMagick).each { |gem| require gem }

require 'vc-grit'
require 'vc-transduction'

module VC
  settings = IO.read("#{File.dirname(__FILE__)}/../settings.json")
  @settings = JSON.parse(settings)

  x = @settings["cache-image-size"]
  @settings["geometry"] = Magick::Geometry.new x, x, nil, nil, Magick::GreaterGeometry

  def self.settings(setting=nil)
    if setting
      @settings[setting] #if defined? setting 
    else
      @settings.to_s
    end
  end
  
end
