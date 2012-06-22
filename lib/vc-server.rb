dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "..", "views")
$:.unshift File.join(dir, "lib")
$:.unshift File.join(dir, "..")

require 'visualculture'

module VC
  class Server < Sinatra::Base
    set :public_folder, File.dirname(__FILE__) + '/..' + '/public'
    set :views, File.dirname(__FILE__) + '/..' + '/views'
    register Sinatra::Reloader
    mime_type :binary

    # Methods
    def initialize
      super
      # Get repo-paths from command line (1 or more):
      # or from settings (to be implemented)
      if VC.settings("repositories").length == 0
        raise "No repositories specified on either command-line or in the current config file."
      else  
        repo_paths = VC.settings("repositories")
      end

      # Create a hash to access repos through their slug:
      @repos = {}
      repo_paths.each do |repo_path|
        @repos[File.basename(repo_path, ".git")] = Grit::Repo.new(repo_path)
        # Though creating all git_repo instances at initialisation
        # might be to heavy at some point
      end
      
      @sorted_repos = @repos.values.sort_by {|r| r.last_updated}.reverse
    end

    def get_commit(cat, id, commit_id, path)
      @repo_slug = 'osp' + '.' + cat + '.' + id
      @repo_path = cat + '/' + id
      @repo = @repos[@repo_slug]
      if commit_id == "latest"
        @commit = @repo.commit('HEAD')
        @commit_slug = "latest"
      else
        @commit = @repo.commit(commit_id)
        @commit_slug = @commit.id[0..10]
      end
      halt "No commit exists with id #{commit_id}" if @commit.nil?
      @object = (path == "" ? @commit.tree : @commit.tree / path)
      halt "No object exists with path #{path}" if @object.nil?
      
      # Set title
      if @repo
        @title += " :: " + @repo.category.capitalize + " :: " + @repo.title
      end
      if @commit
        @title += " :: " + ( @object.name ? @object.name : "/" )  + " @ " + @commit_slug 
      end
    end

    # Routes
    before do
      @title = VC.settings("title")
    end

    get "/" do
      erb :repos
    end

    get "/:cat/" do |cat|
      @title += " :: " + cat.capitalize
      @cat = cat
      erb :category
    end

    get "/:cat/:id/" do |cat, id|
      @repo_path = cat + '/' + id
      @repo_slug = 'osp' + '.' + cat + '.' + id
      @repo = @repos[@repo_slug]
      @title += " :: " + @repo.category.capitalize + " :: " + @repo.title
      erb :index
    end

    get "/:cat/:id/repo.json" do |cat, id|
      content_type "text/plain"
      @repo_path = cat + '/' + id
      @repo_slug = 'osp' + '.' + cat + '.' + id
      @repos[@repo_slug].to_json
    end

    get "/settings" do
    end

    get "/:cat/:id/render/:commit_id/*" do |cat, id, commit_id, path|
      get_commit cat, id, commit_id, path
      x = @object.transduce VC.settings("preview-image-size")
      if x
        send_file x
      else
        redirect "http://placehold.it/770x770&text=" + @object.name
      end
    end

    get "/:cat/:id/thumbnail/:commit_id/*" do |cat, id, commit_id, path|
      get_commit cat, id, commit_id, path
      if @object.is_a? Grit::Blob
        x = @object.transduce VC.settings("thumb-image-size")
        if x
          send_file x
        else
          redirect "http://placehold.it/180&text=" + @object.name
        end
      else
        # It’s a folder
        redirect "http://placehold.it/180&text=" + @object.name
      end
    end

    get "/:cat/:id/view/:commit_id/*" do |cat, id, commit_id, path|
      get_commit cat, id, commit_id, path
      if @object.is_a? Grit::Blob
        # Blob
        @path = path
        erb :blob
      else
        # Folder
        @tree = @object
        if path == ""
          @path = path
        else
          @path = path + "/"
        end
        @dir = true
        erb :dir
      end
    end

    get "/:cat/:id/raw/:commit_id/*" do |cat, id, commit_id, path|
      get_commit cat, id, commit_id, path
      if @object.is_a? Grit::Blob
        content_type @object.mime_type
        @object.data
      else
        halt "to implement raw tree?"
      end
    end
    
    # sweet, an api
    get "/repos.json" do
      content_type "text/plain"
      @repos.values.map {|repo| repo.to_hash}.sort_by {|r| r['last_updated']}.reverse.to_json 
    end
    
    get "/commits.json" do
      content_type "text/plain"
      commits = []
      @repos.values.each do |repo|
        commits += repo.commit_overview
      end
      commits.sort_by {|r| r['date_iso']}[-10..-1].reverse.to_json 
    end
    
  end
end