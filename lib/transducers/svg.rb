# SVG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    svg = lambda {|blob, size|
      ret = []
      tmpsvg = File.join( VC.settings("cache-dir"), "#{blob.id[0..10]}.svg" )
      File.open(tmpsvg, 'w') do |f|
        f.write blob.data
      end
      name = blob.compose_path_2(size) 
      w = %x[inkscape -W #{tmpsvg}]
      h = %x[inkscape -H #{tmpsvg}]
      x = w > h ? "-w" : "-h"
      %x[inkscape #{tmpsvg} -D --export-png=#{name} #{x} #{size}]
      name
    }    
    @handlers["image/svg+xml"] = svg
    @extensions["image/svg+xml"] = '.png'
  end
end
