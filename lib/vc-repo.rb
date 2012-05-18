module VC
  module RepoHelper
    def slug
      components = self.path.split('/')
      if components.last == ".git"
        components[-2]
      else
        components[-1].sub('.git','')
      end
    end
    def web_path
      self.slug.split('.')[-2..-1].join('/')
    end
    def _readme
      readme_file = self.tree.contents.map {|x| x.name.include?('README') ? x.name : nil}.compact.first
      (self.tree / readme_file).data
    end
    def title
      if self._readme
        self._readme.lines.first.chomp
      else
        nil
      end
    end
    def project_description
      if self._readme
        # Take the introductory text from the README
        # And convert it to html
        m = RDiscount.new self._readme.split('- - -')[0]
        m.to_html
      else
        nil
      end
    end
    def iceberg
      iceberg = (self.tree / "iceberg")
      if iceberg.nil?
        return nil
      end      
      iceberg.contents.map {|x| /jpg|jpeg|png|gif/i.match(x.name) ? x.name : nil}.compact
    end
    def source_files
      # If there's only 2, that means just the README and the iceberg
      # i.e. only presentation, not source files
      self.tree.contents.length > 2
    end
    def blog_post
      nil
    end
    def gallery
      nil
    end
    def commit_overview
      self.commits.map {|commit| { 'id' => commit.id[0..10], 'author' => commit.author, 'date' => commit.committed_date, 'message' => commit.message, 'message_short' => commit.message.lines.first }}
    end
    def to_json
      {'slug' => self.slug, 'web_path' => self.web_path, 'title' => self.title, 'project_description' => self.project_description, 'iceberg' => self.iceberg, 'commits' => self.commit_overview, 'blog_post' => self.blog_post, 'gallery' => self.gallery, 'source_files' => self.source_files}.to_json
    end
  end
end
