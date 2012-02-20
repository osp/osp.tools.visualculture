# Implemenation (could it really be this easy? -- it turns out it is!!!)
$: << "/home/serk17/osp/osp.tools.visualculture.test/"
require 'visualculture'


module VC

  def self.transduce(blob, s=nil)
      handlers = VC::Transducers.handlers
      if handlers[blob.mime_type]
        sizes = s.nil? ? VC.settings("image-sizes") : s
        handlers[blob.mime_type].call(blob, sizes)
      else
        nil
      end
  end

  def self.transducer?(blob)
    handlers = VC::Transducers.handlers
    handlers[blob.mime_type] ? true : false
  end  


  module Transducers
    include Magick
    @handlers = {}
    
    def self.handlers
      @handlers
    end
    
    def transduce(s=nil)
      handlers = VC::Transducers.handlers
      if handlers[self.mime_type]
        sizes = s.nil? ? VC.settings("image-sizes") : s
        handlers[self.mime_type].call(self, sizes)
      else
        nil
      end
    end
    
    def transducer?
      handlers = VC::Transducers.handlers
      handlers[self.mime_type] ? true : false
    end     
  end
end
