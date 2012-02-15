# Implemenation (could it really be this easy? -- it turns out it is!!!)
$: << "/home/serk17/osp/osp.tools.visualculture.test/"

module VC
  module Transducers
    include Magick
    @handlers = {}
    def self.transduce(blob, name=nil, sizes=nil)
      @handlers[blob.mime_type].call(blob, name, sizes)
    end
  end
end
