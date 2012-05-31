# SVG transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    otf = lambda {|blob, size|
      tmpfnt = File.join( VC.settings("cache-dir"), "#{blob.id[0..10]}.otf")
      File.open(tmpfnt, 'w') do |f|
        f.write blob.data
      end
      name =  blob.compose_path_2
      w = size.to_i
      h = (w * 0.75).to_i # So thats kind of arbitrary but it gives good results in general
      %x[convert -font #{tmpfnt} -background transparent -gravity center -size #{w}x#{h} label:'Aa' #{name}]
      name
    }    
    @handlers["application/opentype"] = otf
    @extensions["application/opentype"] = '.png'
  end
end
