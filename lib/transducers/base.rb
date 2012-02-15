# Implemenation (could it really be this easy? -- it turns out it is!!!)
$: << "/home/serk17/osp/osp.tools.visualculture.test/"
require 'visualculture'


module VC

  def self.transduce(blob, s=nil)
    sizes = s.nil? ? VC.settings("image-sizes") : s
    handlers = VC::Transducers.handlers
    handlers[blob.mime_type].call(blob, sizes)
  end


  module Transducers
    include Magick
    @handlers = {}
    
    def self.handlers
      @handlers
    end
    
    def transduce(blob, sizes=[])
      handlers = VC::Transducers.handlers
      handlers[blob.mime_type].call(blob, sizes)
    end
  end
end
