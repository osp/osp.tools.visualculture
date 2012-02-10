$:.unshift File.join(File.dirname(__FILE__), ".." , "lib")
require 'minitest/autorun'

require 'visualculture'

describe Grit::Blob do
  before do
    @repo = Grit::Repo.new('/home/serk17/osp/osp.tools.visualculture.test')
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
    
    it "should be transduct successfully" do
      VC::Transducers.transduce(@png).must_equal "success!"
    end
  end
  
  # JPEG  
  describe "when the blob is a jpg" do
    it "should return the correct mimetype" do
      @jpg.mime_type.must_equal "image/jpeg"
    end
    
    it "should be transduct successfully" do
      VC::Transducers.transduce(@jpg).must_equal "success!"
    end
  end 

  # GIF
  describe "when the blob is a gif" do
    it "should return the correct mimetype" do
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should be transduct successfully" do
      skip("Not implemented yet...")
      VC::Transducers.transduce(@jpg).must_equal "success!"
    end
  end
  
  # SVG
  describe "when the blob is an svg" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should be transduct successfully" do
      skip("Not implemented yet...")
      VC::Transducers.transduce(@jpg).must_equal "success!"
    end
  end
  
  # PostScript
  describe "when the blob is postscript" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should be transduct successfully" do
      skip("Not implemented yet...")
      VC::Transducers.transduce(@jpg).must_equal "success!"
    end
  end
  
  # Scribus
  describe "when the blob is a sla" do
    it "should return the correct mimetype" do
      skip("Not implemented yet...")
      @gif.mime_type.must_equal "image/gif"
    end
    
    it "should be transduct successfully" do
      skip("Not implemented yet...")
      VC::Transducers.transduce(@jpg).must_equal "success!"
    end
  end
end
