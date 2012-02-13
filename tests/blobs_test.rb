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
  end

  # PNG
  describe "when the blob is a png" do
    it "should return the correct mimetype" do
      @png.mime_type.must_equal "image/png"
    end
    
    it "should transduct and still have the correct mime type" do
      v = Linguist::FileBlob.new VC::Transducers.transduce @png
      v.mime_type.must_equal "image/png"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read VC::Transducers.transduce @png
      [v[0].columns, v[0].rows].must_include VC.settings("cache-image-size").to_i
    end
  end
  
  # JPEG  
  describe "when the blob is a jpg" do
    it "should return the correct mimetype" do
      @jpg.mime_type.must_equal "image/jpeg"
    end
    
    it "should transduct into a jpg" do
      v = Linguist::FileBlob.new VC::Transducers.transduce @jpg
      v.mime_type.must_equal "image/jpeg"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read VC::Transducers.transduce @jpg
      [v[0].columns, v[0].rows].must_include VC.settings("cache-image-size").to_i
    end
  end 

  # GIF
  describe "when the blob is a gif" do
    it "should return the correct mimetype" do
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should transduct into a gif" do
      v = Linguist::FileBlob.new VC::Transducers.transduce @gif
      v.mime_type.must_equal "image/gif"
    end
    
    it "should emerge with either correct width or height" do
      v = Magick::Image.read VC::Transducers.transduce @gif
      [v[0].columns, v[0].rows].must_include VC.settings("cache-image-size").to_i
    end
  end
  
  # SVG
  describe "when the blob is an svg" do
  end
  
  # PostScript
  describe "when the blob is postscript" do
  end
  
  # Scribus
  describe "when the blob is a sla" do
  end
end
