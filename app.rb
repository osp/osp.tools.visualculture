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

def get_commit(commit_id, path)
  @repo = settings.repo
  @commit = @repo.commit(commit_id)
  halt "No commit exists with id #{commit_id}" if @commit.nil?
	@object = path == "" ? @commit.tree : @commit.tree / path 
  halt "No object exists with path #{path}" if @object.nil?
end

get "/" do
  @commits = settings.repo.commits
  erb :index
end

get "/settings" do
end

get "/render/:commit_id/*" do |commit_id, path|
  get_commit commit_id, path
  x = @object.transduce VC.settings("preview-image-size")
  if x
    send_file x.first
  else
    redirect "http://placehold.it/770x770&text=" + @object.name
  end
end

get "/thumbnail/:commit_id/*" do |commit_id, path|
  get_commit commit_id, path
  if @object.is_a? Grit::Blob
    x = @object.transduce VC.settings("thumb-image-size")
    if x
      send_file x.first
    else
      redirect "http://placehold.it/180&text=" + @object.name
    end
  else
    # It’s a folder
    redirect "http://placehold.it/180&text=" + @object.name
  end
end

get "/view/:commit_id/*" do |commit_id, path|
  get_commit commit_id, path
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

get "/raw/:commit_id/*" do |commit_id, path|
  get_commit commit_id, path
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
