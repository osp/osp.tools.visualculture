# PNG transducer

module VC
  module Transducers
    png = lambda {|blob|
      r = Image.from_blob(blob.data)
      r[0].adaptive_resize(0.5)
      r[0].write(VC.settings("cache-dir") + "really.png")
      VC.settings("cache-dir") + "really.png"
    }
    @handlers["image/png"] = png
  end
end
