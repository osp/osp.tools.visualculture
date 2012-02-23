module VC

	module CacheHelper

		def cached?

		end

		def compose_path(commit=nil, size=nil)
			commit = commit.nil? ? self.blame[0].id : commit.id
			ext = VC::Transducers.extensions[self.mime_type] ? VC::Transducers.extensions[self.mime_type] : File.extname self.name
			new_name = File.basename(self.name, File.extname self.name) + ext
			path = VC.settings("cache-dir") + commit[0..10] + "/" + size.to_s + "/" + new_name
		end

		def cache(size=nil)
			self.transduce
		end

	end

end
