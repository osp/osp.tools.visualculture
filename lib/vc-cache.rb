module VC
  module CacheHelper
    def cached?(size=nil)
      size = size.nil? ? VC.settings("preview-image-size") : size
      File.exist? self.compose_path_2(size)
    end

    def compose_path_2(size=nil)
      size = size.nil? ? VC.settings("thumb-image-size").to_i : size
      cache_commit_dir = File.join( VC.settings("cache-dir"), 'blobs', self.id[0..10] )
      ext = VC::Transducers.extensions[self.mime_type] ? VC::Transducers.extensions[self.mime_type] : File.extname(self.name)
      new_name = File.basename(self.name, File.extname(self.name)) + ext
      File.join( cache_commit_dir, size.to_s, new_name )
    end


  end
end
