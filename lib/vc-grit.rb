# Here we include Visual Culture-specific mixins and modules into the Grit ecosystem

module Grit
  class Blob
    include Linguist::BlobHelper
    include VC::TransductionHelper
    include VC::CacheHelper
  end
end
