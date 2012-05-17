module VC
  module RepoHelper
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
    def to_json
      {'title' => self.title, 'project_description' => self.project_description, 'iceberg' => self.iceberg}.to_json
    end
  end
end
