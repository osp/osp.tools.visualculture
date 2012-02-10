# JPG transducer

module VC
  module Transducers
    jpg = lambda {|blob|
      "success!"
    }
    @handlers["image/jpeg"] = jpg
  end
end
