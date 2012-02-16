$:.unshift File.join(File.dirname(__FILE__), ".." , "lib")
require 'minitest/autorun'
require 'minitest/pride'

require 'visualculture'

describe Grit::Blob do

  before do
    @repo = Grit::Repo.new VC.settings("test-dir")
    @commit = @repo.commits.first
    @png = @commit.tree / "test_blobs/png.png"
    @jpg = @commit.tree / "test_blobs/jpg.jpg"
    @gif = @commit.tree / "test_blobs/gif.gif"
    @svg = @commit.tree / "test_blobs/svg.svg"
  end

  # PNG
  describe "when the blob is a png" do
    it "should return the correct mimetype" do
      @png.mime_type.must_equal "image/png"
    end
    
    it "should transduct and still have the correct mime type" do
      v = Linguist::FileBlob.new (VC.transduce @png, [VC.settings("preview-image-size")]).first
      v.mime_type.must_equal "image/png"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read (VC.transduce @png, [VC.settings("preview-image-size")]).first
      [v[0].columns, v[0].rows].must_include VC.settings("preview-image-size").to_i
    end
    
    it "should transduct into VC.settings-defined sizes by default" do
      v = @png.transduce
      v.length.must_equal VC.settings("image-sizes").length
    end
    
    it "should transduct to every size requested" do
      v = VC.transduce @png, [48,96,128]
      v.length.must_equal [48,96,128].length
    end
    
  end
  
  # JPEG  
  describe "when the blob is a jpg" do
    it "should return the correct mimetype" do
      @jpg.mime_type.must_equal "image/jpeg"
    end
    
    it "should transduct into a jpg" do
      v = Linguist::FileBlob.new (VC.transduce @jpg, [VC.settings("preview-image-size")]).first
      v.mime_type.must_equal "image/jpeg"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read (VC.transduce @jpg, [VC.settings("preview-image-size")]).first
      [v[0].columns, v[0].rows].must_include VC.settings("preview-image-size").to_i
    end

    it "should transduct into VC.settings-defined sizes by default" do
      v = VC.transduce @jpg
      v.length.must_equal VC.settings("image-sizes").length
    end
    
    it "should transduct to every size requested" do
      v = VC.transduce @jpg, [48,96,128]
      v.length.must_equal [48,96,128].length
    end
  end 

  # GIF
  describe "when the blob is a gif" do
    it "should return the correct mimetype" do
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should transduct into a gif" do
      v = Linguist::FileBlob.new (VC.transduce @gif, [VC.settings("preview-image-size")]).first
      v.mime_type.must_equal "image/gif"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read (VC.transduce @gif, [VC.settings("preview-image-size")]).first
      [v[0].columns, v[0].rows].must_include VC.settings("preview-image-size").to_i
    end
    
    it "should transduct into VC.settings-defined sizes by default" do
      v = VC.transduce @gif
      v.length.must_equal VC.settings("image-sizes").length
    end
    
    it "should transduct to every size requested" do
      v = VC.transduce @gif, [48,96,128]
      v.length.must_equal [48,96,128].length
    end
  end
  
  # SVG
  describe "when the blob is an svg" do    
    it "should return the correct mimetype" do
      @svg.mime_type.must_equal "image/svg+xml"
    end
    
    it "should transduct into a png" do
      v = Linguist::FileBlob.new (VC.transduce @svg, [VC.settings("preview-image-size")]).first
      v.mime_type.must_equal "image/png"
    end

    it "should transduct into VC.settings-defined sizes by default" do
      v = VC.transduce @svg
      v.length.must_equal VC.settings("image-sizes").length
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read (VC.transduce @svg, [VC.settings("preview-image-size")]).first
      [v[0].columns, v[0].rows].must_include VC.settings("preview-image-size").to_i
    end
    
    it "should transduct to every size requested" do
      v = VC.transduce @svg, [48,96,128]
      v.length.must_equal [48,96,128].length
    end
  end
  
  # PostScript
  describe "when the blob is postscript" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
    end
    
    it "should transduct into a gif" do
      skip("Not implemented yet...")
    end

    it "should transduct into VC.settings-defined sizes by default" do
      skip("Not implemented yet...")
    end
    
    it "should emerge with either correct width or height" do
      skip("Not implemented yet...")
    end
    
    it "should transduct to every size requested" do
      skip("Not implemented yet...")
    end
  end
  
  # Scribus
  describe "when the blob is a sla" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
    end
    
    it "should transduct into a gif" do
      skip("Not implemented yet...")
    end

    it "should transduct into VC.settings-defined sizes by default" do
      skip("Not implemented yet...")
    end
    
    it "should emerge with either correct width or height" do
      skip("Not implemented yet...")
    end
    
    it "should transduct to every size requested" do
      skip("Not implemented yet...")
    end
  end
  
  # TTF
  describe "when the blob is a TrueType font" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
    end
    
    it "should transduct into a gif" do
      skip("Not implemented yet...")
    end

    it "should transduct into VC.settings-defined sizes by default" do
      skip("Not implemented yet...")
    end
    
    it "should emerge with either correct width or height" do
      skip("Not implemented yet...")
    end
    
    it "should transduct to every size requested" do
      skip("Not implemented yet...")
    end
  end

  # OTF
  describe "when the blob is an OpenType font" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
    end
    
    it "should transduct into a gif" do
      skip("Not implemented yet...")
    end

    it "should transduct into VC.settings-defined sizes by default" do
      skip("Not implemented yet...")
    end
    
    it "should emerge with either correct width or height" do
      skip("Not implemented yet...")
    end
    
    it "should transduct to every size requested" do
      skip("Not implemented yet...")
    end
  end  

  # UFO
  describe "when the blob is a UFO" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
    end
    
    it "should transduct into a gif" do
      skip("Not implemented yet...")
    end

    it "should transduct into VC.settings-defined sizes by default" do
      skip("Not implemented yet...")
    end
    
    it "should emerge with either correct width or height" do
      skip("Not implemented yet...")
    end
    
    it "should transduct to every size requested" do
      skip("Not implemented yet...")
    end
  end

end
