require 'visualculture'

module VC
  module Transducers
    include Magick
    @handlers = {}
    @extensions = {}
    
    def self.handlers
      @handlers
    end

    def self.extensions
      @extensions
    end
  end
end
