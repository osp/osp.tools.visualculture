# GIF transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    gif = lambda {|blob, sizes|
      r = ImageList.new       # ImageLists need initialization before from_blob
      ret = []
      name = File.basename blob.name, blob.extname
      sizes.each do |size|
        r.from_blob(blob.data)
        geometry = Geometry.new size, size, nil, nil, GreaterGeometry
        r.each do |x|
          x.change_geometry! geometry do |h,w,img|
            img.resize! h,w
          end
        end
        r.write VC.settings("cache-dir") + name + size.to_s + ".gif"
        ret << VC.settings("cache-dir") + name + size.to_s + ".gif"
      end
      ret
    }  
    @handlers["image/gif"] = gif
  end
end
