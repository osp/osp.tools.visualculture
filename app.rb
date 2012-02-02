%w(sinatra grit linguist).each { |gem| require gem }

mime_type :binary, 'binary/octet-stream'
set :repo, Grit::Repo.new(ARGV[1])

before %r{^/(\w+)} do
  commit_id = params[:captures].first[0..10]
  @commit = settings.repo.commits(commit_id).first
  halt "No commit exists with id #{commit_id}" if @commit.nil?
end

get "/" do
  @commits = settings.repo.commits
  haml :index
end

get "/:commit_id" do |commit_id|
  @tree = @commit.tree
  @path = ""
  haml :dir
end

get "/:commit_id/*" do |commit_id, path|
  @object = @commit.tree / path
  halt "No object exists with path #{path}" if @object.nil?
  if @object.is_a? Grit::Blob
    content_type :binary
    @object.data
  else
    @tree = @object
    @path = path + "/"
    haml :dir
  end
end

__END__

@@ index
%ul
  - @commits.each do |commit|
    %li
      %a{ :href => "/#{commit.id[0..10]}" }= "#{commit.id[0..10]} (by #{commit.author}, #{commit.committed_date})"

@@ dir
%h1= "Commit #{@commit.id[0..10]} - Path: #{@path}"
%ul
  - @tree.contents.each do |obj|
    %li
      %a{ :href => "/#{@commit.id}/#{@path}#{obj.name}" }= obj.name

