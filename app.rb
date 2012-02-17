dir = File.dirname(__FILE__)
$:.unshift File.join(dir, "views")
$:.unshift File.join(dir, "lib")

require 'visualculture'

mime_type :binary, 'binary/octet-stream'
set :repo, Grit::Repo.new(ARGV[1])
set :config, JSON.parse(IO.read "#{File.dirname(__FILE__)}/settings.json")

before do
  @repo_name = ARGV[1].split("/")[-1]
  @title = VC.settings("title")
end

def get_commit commit_id
  @repo = settings.repo
  p @repo.commits
  @commit = @repo.commits(commit_id).first
  @title = VC.settings("title")
  halt "No commit exists with id #{commit_id}" if @commit.nil?
  @dir = nil
end

get "/" do
  @commits = settings.repo.commits
  erb :index
end

get "/render/:commit_id/*" do |commit_id, path|
  get_commit commit_id
  @object = @commit.tree / path
  halt "No object exists with path #{path}" if @object.nil?
  x = VC::transduce(@object)
  if x
    send_file x[0]
  else
    redirect "http://placehold.it/770x770&text=" + @object.name
  end
end

get "/thumbnail/:commit_id/*" do |commit_id, path|
  get_commit commit_id
  @object = @commit.tree / path
  halt "No object exists with path #{path}" if @object.nil?
  if @object.is_a? Grit::Blob
    x = VC::transduce(@object)
    if x
      send_file x[1]
    else
      redirect "http://placehold.it/180&text=" + @object.name
    end
  else
    # It’s a folder
    redirect "http://placehold.it/180&text=" + @object.name
  end
end

get "/view/:commit_id/*" do |commit_id, path|
  get_commit commit_id
  if path == ""
    # Root
    @tree = @commit.tree
    @path = ""
    @dir = true
    erb :dir
  else
    @object = @commit.tree / path
    halt "No object exists with path #{path}" if @object.nil?
    if @object.is_a? Grit::Blob
      # Blob
      @path = path
      erb :blob
    else
      # Folder
      @tree = @object
      @path = path + "/"
      @dir = true
      erb :dir
    end
  end
end

get "/raw/:commit_id/*" do |commit_id, path|
  get_commit commit_id
  @object = @commit.tree / path
  halt "No object exists with path #{path}" if @object.nil?
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