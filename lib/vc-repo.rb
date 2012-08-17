# encoding: UTF-8
module VC
  module RepoHelper
    def slug
      # use the path to the repo to find the slug:
      components = self.path.split('/')
      if components.last == ".git"
        # checked out repo
        # /home/o/osp/osp.work.bessst/.git(/) -> osp.work.bessst
        components[-2]
      else
        # bare repo
        # /home/o/osp/osp.work.bessst.git(/) -> osp.work.bessst
        components[-1].sub('.git','')
      end
    end
    def web_path
      # 'osp.tools.visualculture' -> 'tools/visualculture'
      # 'osp.tools.visualculture.test' -> 'tools/visualculture.test'
      # 'osp.work.balsamine.2011-2012' -> 'work/balsamine.2011-2012'
      # should think of some exception if there’s no dot
      components = self.slug.split('.')
      [components[1], components[2..-1].join('.')].join('/')
    end
    def web_url
      # where to find this repo on the web:
      # http://ospwork.constantvzw.org/work/balsamine.2011-2012/
      VC.settings("web-domain") + self.web_path + '/'
    end
    def category
      # 'osp.tools.visualculture' -> 'tools'
      # In ruby, this will return nil if there’s no dots in the slug
      # should think of some exception in python
      self.slug.split('.')[1]
    end
    def _readme
      # look at the root tree for a filename that looks like README
      # and return it’s contents
      readme_file = self.tree.contents.map {|x| x.name.include?('README') ? x.name : nil}.compact.first
      f = (self.tree / readme_file)
      if f.nil?
        nil
      else
        begin
          f.data.force_encoding("UTF-8")
        rescue NoMethodError
          f.data
        end
      end
    end
    def title
      # The title is usually the first line of the README
      if self._readme
        self._readme.lines.first.chomp
      else
        # 'osp.tools.visualculture' -> 'visualculture'
        self.slug.split('.').last
      end
    end
    def project_description
      if self._readme
        # Returns the introductory text from the README
        # converted to html
        # (this pressuposes the readme is markdown,
        # and that the introduction is demarcated from the rest by
        # '- - -')
        m = RDiscount.new self._readme.split('- - -')[0]
        m.to_html
      else
        "<p>Please insert a project description</p>"
      end
    end
    def iceberg
      iceberg = (self.tree / "iceberg")
      if iceberg.nil?
        return nil
      end
      # return all image files in the iceberg folder:
      # (we could return other types of files as well, since you can access their rendered preview)
      # (the ruby version had problems with symbolic links, by the way)
      iceberg.contents.map {|x| /jpg|jpeg|png|gif/i.match(x.name) ? x.name : nil}.compact
    end
    def source_files
      # If there's only 2 items in the root tree,
      # that likely means just the README file and the iceberg folder
      # as is still the case with some of the old projects imported from Indexhibit
      # in this case self.source_files = false
      self.tree.contents.length > 2
    end
    def blog_post
      # I figured to scan the readme for links to blog posts
      # not implemented
      nil
    end
    def gallery
      # I figured to scan the readme for links to the gallery3
      # not implemented
      nil
    end
    def commit_overview
      # A hash of recent commits with elementary info, to be attached to the repo object in the api
      begin
        self.commits.map {|commit| { 'id' => commit.id[0..10], 'author' => commit.author.name.force_encoding("UTF-8"), 'date' => commit.committed_date, 'date_iso' => commit.committed_date.xmlschema, 'message' => commit.message.force_encoding("UTF-8"), 'message_short' => commit.message.lines.first.force_encoding("UTF-8"), 'parent_repo_slug' => self.slug, 'parent_repo_title' => self.title, 'parent_repo_url' => self.web_url }}
      rescue NoMethodError
        self.commits.map {|commit| { 'id' => commit.id[0..10], 'author' => commit.author.name, 'date' => commit.committed_date, 'date_iso' => commit.committed_date.xmlschema, 'message' => commit.message, 'message_short' => commit.message.lines.first, 'parent_repo_slug' => self.slug, 'parent_repo_title' => self.title, 'parent_repo_url' => self.web_url }}
      end 
    end
    def last_updated
      # last updated in ISO 
      self.commit('HEAD').date.xmlschema
    end
    def recent
      # Steph would like to know,
      # has the repo been updated last month (approximately)? 
      if Time.now() - self.commit('HEAD').date < 30 * 24 * 60 * 60
        true
      else
        nil
      end
    end
    def html_classes
      # inspired by P.M.’s suggestion to add plenty of classes that can be useful
      # when styling…
      # this loops over a number of properties of the repo, and if they turn
      # out to be true, adds them to a list of space separated classes that
      # can be easily used in an HTML template
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
      # create a hash to serialise as a JSON object for the api
      {'slug' => self.slug, 'web_path' => self.web_path, 'web_url' => self.web_url, 'title' => self.title, 'project_description' => self.project_description, 'iceberg' => self.iceberg, 'commits' => self.commit_overview, 'blog_post' => self.blog_post, 'gallery' => self.gallery, 'source_files' => self.source_files, 'html_classes' => self.html_classes, 'last_updated' => self.last_updated}
    end
    def to_json
      self.to_hash.to_json
    end
  end
end
