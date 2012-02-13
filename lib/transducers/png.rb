# PNG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    png = lambda {|blob|
      r = Image.from_blob(blob.data)
      x = r[0].change_geometry VC.settings("geometry") do |h,w,img|
        img.resize! h,w
      end
      x.write(VC.settings("cache-dir") + "really.png")
      VC.settings("cache-dir") + "really.png"
    }
    @handlers["image/png"] = png
  end
end
