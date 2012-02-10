# PNG transducer

module VC
  module Transducers
    png = lambda {|blob|
      r = Image.from_blob(blob.data)
      r[0].adaptive_resize(0.5)
      r[0].write("/tmp/really.png")
      "/tmp/really.png"
    }
    @handlers["image/png"] = png
  end
end
