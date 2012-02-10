$:.unshift File.join(File.dirname(__FILE__))
%w(sinatra grit linguist).each { |gem| require gem }

require 'lib/vc-repo'

mime_type :binary, 'binary/octet-stream'
set :repo, Grit::Repo.new(ARGV[1])

before %r{^/(\w+)} do
  commit_id = params[:captures].first[0..10]
  @commit = settings.repo.commits(commit_id).first
  @title = "OSP Visual Culture Git Viewer"
  halt "No commit exists with id #{commit_id}" if @commit.nil?
end

get "/" do
  @commits = settings.repo.commits
  erb :index
end

get "/:commit_id" do |commit_id|
  @tree = @commit.tree
  @path = ""
  erb :dir
end

get "/:commit_id/*" do |commit_id, path|
  @object = @commit.tree / path
  halt "No object exists with path #{path}" if @object.nil?
  if @object.is_a? Grit::Blob
    p "cool!"
    if @object.binary?
      p "it's binary!"
      content_type :binary
    end
    @object.data
  else
    @tree = @object
    @path = path + "/"
    erb :dir
  end
end
