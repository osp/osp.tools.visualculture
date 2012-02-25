require 'transducers/base'
require 'transducers/png'
require 'transducers/jpg'
require 'transducers/gif'
require 'transducers/svg'

module VC
  def self.transduce(blob, s=nil)
    if VC::Transducers.handlers[blob.mime_type]
      sizes = s.nil? ? VC.settings("image-sizes") : s
      VC::Transducers.handlers[blob.mime_type].call(blob, sizes)
    else
      nil
    end
  end

  def self.transducer?(blob)
    VC::Transducers.handlers[blob.mime_type] ? true : false
  end  
end

module VC
	module TransductionHelper
    def transduce(s=nil)
      if VC::Transducers.handlers[self.mime_type]
        sizes = s.nil? ? VC.settings("image-sizes") : [s]
        VC::Transducers.handlers[self.mime_type].call(self, sizes)
      else
        nil
      end
    end
    
    def transducer?
      VC::Transducers.handlers[self.mime_type] ? true : false
    end
	end
end
