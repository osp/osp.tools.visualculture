# encoding: UTF-8
# PDF transducer
$:.unshift File.join(File.dirname(__FILE__), "..")
require 'visualculture'

require 'cairo'
require 'poppler'

module VC
  module Transducers
	  begin
  require 'gtk2'
rescue Gtk::InitError
end
    pdf = lambda {|blob, size|
	name = blob.compose_path_2(size)
	tmpf = File.join( VC.settings("cache-dir"), "#{blob.id[0..10]}.pdf")
	File.open(tmpf, 'w') do |f|
		f.write blob.data
	end
	surf = Cairo::ImageSurface.new(size.to_i,size.to_i)
	ctx = Cairo::Context.new(surf)
	doc = Poppler::Document.new(tmpf)
	page = doc.get_page(0)
	page.render(ctx)
	surf.write_to_png(name)
        name
    }    
    @handlers["application/pdf"] = pdf
    @extensions["application/pdf"] = '.png'
  end
end
