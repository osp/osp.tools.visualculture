# JPG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    jpg = lambda {|blob, sizes|
      r = Image.from_blob(blob.data)
      ret = []
      name = File.basename blob.name, blob.extname
      sizes.each do |size|
        geometry = Geometry.new size, size, nil, nil, GreaterGeometry
        x = r[0].change_geometry geometry do |h,w,img|
          img.resize! h,w
        end
        x.write VC.settings("cache-dir") + name + size.to_s + ".jpg"
        ret << VC.settings("cache-dir") + name + size.to_s + ".jpg"
      end
      ret
    }
    @handlers["image/jpeg"] = jpg
  end
end
