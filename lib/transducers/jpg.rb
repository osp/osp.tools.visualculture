# JPG transducer

module VC
  module Transducers
    jpg = lambda {|blob|
      r = Image.from_blob(blob.data)
      r[0].adaptive_resize(0.5)
      r[0].write(VC.settings("cache-dir") + "really.jpg")
      VC.settings("cache-dir") + "really.jpg"
    }
    @handlers["image/jpeg"] = jpg
  end
end
