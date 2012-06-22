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
      components = self.slug.split('.')
      [components[1], components[2..-1].join('.')].join('/')
    end
    def web_url
      VC.settings("web-domain") + self.web_path + '/'
    end
    def category
      self.slug.split('.')[1]
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
      self.commits.map {|commit| { 'id' => commit.id[0..10], 'author' => commit.author, 'date' => commit.committed_date, 'date_iso' => commit.committed_date.xmlschema, 'message' => commit.message, 'message_short' => commit.message.lines.first, 'parent_repo_slug' => self.slug, 'parent_repo_title' => self.title, 'parent_repo_url' => self.web_url }}
    end
    def last_updated
      self.commit('HEAD').date.xmlschema
    end
    def recent
      if Time.now() - self.commit('HEAD').date < 30 * 24 * 60 * 60
        true
      else
        nil
      end
    end
    def html_classes
      html_classes = []
      methods = ['iceberg', 'blog_post', 'gallery', 'source_files', 'recent']
      methods.each do |m|
        unless self.send(m) == nil
          html_classes << m
        end
      end
      html_classes << self.category
      html_classes.join(' ')
    end
    def to_hash
      {'slug' => self.slug, 'web_path' => self.web_path, 'web_url' => self.web_url, 'title' => self.title, 'project_description' => self.project_description, 'iceberg' => self.iceberg, 'commits' => self.commit_overview, 'blog_post' => self.blog_post, 'gallery' => self.gallery, 'source_files' => self.source_files, 'html_classes' => self.html_classes, 'last_updated' => self.last_updated}
    end
    def to_json
      self.to_hash.to_json
    end
  end
end
