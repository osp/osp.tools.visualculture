require 'open3'

$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

module VC
  module Transducers
    pdf = lambda {|blob, size|
      name = blob.compose_path_2(size)
      r = Image.from_blob(blob.data)
      img = r[0].resize_to_fit(size.to_i, size.to_i)
      img.write name
      name
    }    
    @handlers["application/pdf"] = pdf
    @extensions["application/pdf"] = '.png'
  end
end
