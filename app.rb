dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "views")
$:.unshift File.join(dir, "lib")

require 'visualculture'

mime_type :binary, 'binary/octet-stream'
# Get repo-paths from command line (1 or more):
# or from settings (to be implemented)
repo_paths = ARGV[1..-1]

# Create a hash to access repos through their slug:
@repos = {}
repo_paths.each do |repo_path|
  @repos[File.basename(repo_path, ".git")] = Grit::Repo.new(repo_path)
  # Though creating all git_repo instances at initialisation
  # might be to heavy at some point
end
set :repos, @repos
set :config, JSON.parse(IO.read "#{File.dirname(__FILE__)}/settings.json")

before do
  @title = VC.settings("title")
end

def get_commit(repo_slug, commit_id, path)
  @repo_slug = repo_slug
  @repo = settings.repos[repo_slug]
  @commit = @repo.commit(commit_id)
  halt "No commit exists with id #{commit_id}" if @commit.nil?
  @object = path == "" ? @commit.tree : @commit.tree / path 
  halt "No object exists with path #{path}" if @object.nil?
end

get "/" do
  erb :repos
end

get "/:repo_slug/" do |repo_slug|
  @commits = settings.repos[repo_slug].commits
  @repo_slug = repo_slug
  erb :index
end

get "/settings" do
end

get "/:repo_slug/render/:commit_id/*" do |repo_slug, commit_id, path|
  get_commit repo_slug, commit_id, path
  x = @object.transduce @commit, VC.settings("preview-image-size")
  if x
    send_file x
  else
    redirect "http://placehold.it/770x770&text=" + @object.name
  end
end

get "/:repo_slug/thumbnail/:commit_id/*" do |repo_slug, commit_id, path|
  get_commit repo_slug, commit_id, path
  if @object.is_a? Grit::Blob
    x = @object.transduce @commit, VC.settings("thumb-image-size")
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

get "/:repo_slug/view/:commit_id/*" do |repo_slug, commit_id, path|
  get_commit repo_slug, commit_id, path
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

get "/:repo_slug/raw/:commit_id/*" do |repo_slug, commit_id, path|
  get_commit repo_slug, commit_id, path
  if @object.is_a? Grit::Blob
    if @object.binary?
      content_type :binary
    else
      content_type "text/plain"
    end
    @object.data
  else
    halt "to implement raw tree?"
  end
end
