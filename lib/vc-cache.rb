module VC
	module CacheHelper
		def cached?(commit, size=nil)
			size = size.nil? ? VC.settings("thumb-image-size") : size		
			File.exist? compose_path(commit, size)
		end

		def compose_path(commit, size=nil)
#			commit = self.blame[0].id
			size = size.nil? ? VC.settings("thumb-image-size").to_i : size
			cache_commit_dir = VC.settings("cache-dir") + commit.id[0..10] 
#			unless Dir.exist? cache_commit_dir + "/" + size.to_s
#				unless Dir.exist? cache_commit_dir
#					Dir.mkdir cache_commit_dir
#				end
#				Dir.mkdir cache_commit_dir + size.to_s
#			end
			ext = VC::Transducers.extensions[self.mime_type] ? VC::Transducers.extensions[self.mime_type] : File.extname(self.name)
			new_name = File.basename(self.name, File.extname(self.name)) + ext
			cache_commit_dir + "/" + size.to_s + "/" + new_name
		end

#		def cache(size=nil)
#			self.transduce
#		end

	end
end
