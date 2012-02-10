# PNG transducer

module VC
  module Transducers
    png = lambda {|blob|
      "success!"
    }
    @handlers["image/png"] = png
  end
end
