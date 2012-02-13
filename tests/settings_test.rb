$:.unshift File.join(File.dirname(__FILE__), ".." , "lib")
require 'minitest/autorun'

require 'visualculture'

class TestSetup
  def setup
    include VC
  end
  
#  def test_that_VC_returns_settings
#    assert_equal Hash
end
