$:.unshift File.join(File.dirname(__FILE__), ".." , "lib")
require 'minitest/autorun'

require 'visualculture'

describe Grit::Blob do
  before do
    @repo = Grit::Repo.new('/home/serk17/osp/osp.tools.visualculture.test')
    @commit = @repo.commits.first
    @blob = @commit.tree / "test_blobs/png.png"
  end

  describe "when figuring out what it is" do
    it "should return the correct mimetype" do
      @blob.mime_type.must_equal "image/png"
    end
  end
  
  describe "when transducting" do
    it "should be successful" do
      VC::Transducers.transduce(@blob).must_equal "success!"
    end
  end
end
