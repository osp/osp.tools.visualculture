# SVG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    svg = lambda {|blob, sizes|
      ret = []
      tmpsvg = VC.settings("cache-dir") + "owgod.svg"
      File.open(tmpsvg, 'w') do |f|
        f.write blob.data
      end
      sizes.each do |size|
        name = File.basename(blob.name, blob.extname) + size.to_s + ".png"
        ret <<  VC.settings("cache-dir") + name 
        w = %x[inkscape -W #{tmpsvg}]
        h = %x[inkscape -H #{tmpsvg}]
        x = w > h ? "-w" : "-h"
        system "inkscape #{tmpsvg} -D --export-png=#{VC.settings("cache-dir") + name} #{x} #{size}"
      end
      ret
    }    
    @handlers["image/svg+xml"] = svg
  end
end
