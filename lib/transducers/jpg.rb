# JPG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    jpg = lambda {|blob, size|
      r = Image.from_blob(blob.data)
      name = File.basename blob.name, blob.extname
      geometry = Geometry.new size, size, nil, nil, GreaterGeometry
      x = r[0].change_geometry geometry do |h,w,img|
        img.resize! h,w
      end
      x.write VC.settings("cache-dir") + name + size.to_s + ".jpg"
#			x.write path
			VC.settings("cache-dir") + name + size.to_s + ".jpg"
    }
    @handlers["image/jpeg"] = jpg
  end
end
