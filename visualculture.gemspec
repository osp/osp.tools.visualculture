Gem::Specification.new do |s|
  s.name    = 'visualculture'
  s.version = '0.1.0'
  s.summary = 'A visual git interface oriented towards graphic design workflows'

  s.authors = 'Open Source Publishing'

  s.files = Dir['lib/**/*', 'views/**/*', 'tests/**/*', 'public/**/*', 'settings.json']
  s.executables << 'visualculture'

  s.add_dependency 'sinatra' #, '~> 0.6.6'
  s.add_dependency 'sinatra-contrib' #,    '~> 0.2.3'
  s.add_dependency 'grit' #,      '~> 1.16'
  s.add_dependency 'bundler' #,     '~> 0.2.3'
  s.add_dependency 'json' #,      '~> 1.16'
  s.add_dependency 'rmagick' #,     '~> 0.2.3'
  s.add_dependency 'commander' #,     '~> 0.2.3'
  s.add_development_dependency 'rake'
end
