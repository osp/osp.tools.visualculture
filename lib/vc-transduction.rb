
# Implemenation (could it really be this easy?)
module VC
  module Transducers
    @handlers = {}
    def self.transduce(blob)
      @handlers[blob.mime_type].call(blob)
    end
  end
end


# Adding a handler
module VC
  module Transducers
    png = lambda {|blob|
      "success!"
    }
    @handlers["image/png"] = png
  end
end
