# PNG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    png = lambda {|blob, name, sizes|
      r = Image.from_blob(blob.data)
      ret = []
      sizes.each do |size|
        geometry = Geometry.new size, size, nil, nil, GreaterGeometry
        x = r[0].change_geometry geometry do |h,w,img|
          img.resize! h,w
        end
        x.write VC.settings("cache-dir") + name + "-" + size.to_s + ".png"
        ret << VC.settings("cache-dir") + name + "-" + size.to_s + ".png"
      end
      ret
    }
    @handlers["image/png"] = png
  end
end
