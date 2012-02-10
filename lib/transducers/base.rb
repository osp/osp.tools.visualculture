# Implemenation (could it really be this easy?)
module VC
  module Transducers
    @handlers = {}
    def self.transduce(blob)
      @handlers[blob.mime_type].call(blob)
    end
  end
end
