# SVG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    svg = lambda {|blob, size|
      ret = []
      tmpsvg = VC.settings("cache-dir") + "owgod.svg"
      File.open(tmpsvg, 'w') do |f|
        f.write blob.data
      end
      name = File.basename(blob.name, blob.extname) + size.to_s + ".png" 
      w = %x[inkscape -W #{tmpsvg}]
      h = %x[inkscape -H #{tmpsvg}]
      x = w > h ? "-w" : "-h"
      %x[inkscape #{tmpsvg} -D --export-png=#{VC.settings("cache-dir") + name} #{x} #{size}]
      VC.settings("cache-dir") + name
    }    
    @handlers["image/svg+xml"] = svg
		@extensions["image/svg+xml"] = '.png'
  end
end
