# GIF transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    gif = lambda {|blob, size|
      name = blob.compose_path_2(size)
      r = ImageList.new       # ImageLists need initialization before from_blob
      r.from_blob(blob.data)
      geometry = Geometry.new size.to_i, size.to_i, nil, nil, GreaterGeometry
      r.each do |x|
        x.change_geometry! geometry do |h,w,img|
          img.resize! h,w
        end
      end
      r.write name
      name
    }  
    @handlers["image/gif"] = gif
  end
end
