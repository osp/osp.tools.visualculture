# GIF transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    gif = lambda {|blob|
      r = ImageList.new       # gifs should be processed as ImageList... 
      r.from_blob(blob.data)  # ...and needs to be initialized before blob read
      r.each do |x|
        x.change_geometry! VC.settings("geometry") do |h,w,img|
          img.resize! h,w
        end
      end
      r.write(VC.settings("cache-dir") + "really.gif")
      VC.settings("cache-dir") + "really.gif"
    }  
    @handlers["image/gif"] = gif
  end
end
