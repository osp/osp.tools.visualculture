# Implemenation (could it really be this easy? -- it turns out it is!!!)
#$: << "/home/serk17/osp/osp.tools.visualculture.test/"
require 'visualculture'

module VC
  module Transducers
    include Magick
    @handlers = {}
    
    def self.handlers
      @handlers
    end
  end
end
