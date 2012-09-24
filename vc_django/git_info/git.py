"""
git_info.git


"""


import pygit2
import os

from ordereddict import OrderedDict

try:
	from settings import GIT_ROOT
except Exception:
	print('GIT_ROOT is not defined in your settings, aborting')
	raise

	
class GitRepository(object):
	def __init__(self, fname):
		self.repo = pygit2.Repository(fname)
		
		# We expect a 3 components name: prefix.category.name (eg: osp.work.balsamine)
		# These can be more components when subspecifying:
		# osp.work.balsamine.2011-2012, osp.tools.visualculture.test
		
		# in case of a bare git repository, the folder name will end in .git
		# this is stripped off
		
		self.repo_fullname = os.path.basename(os.path.normpath(fname)).rstrip('.git')
		self.repo_parts = self.repo_fullname.split('.')
		if len(self.repo_parts) > 2:
			self.repo_prefix = self.repo_parts[0]
			self.repo_category = self.repo_parts[1]
			self.repo_name = '.'.join(self.repo_parts[2:])
		else:
			self.repo_prefix = ''
			self.repo_category = ''
			self.repo_name = self.repo_fullname
		
	def has_iceberg(self):
		iceberg_t = None
		try:
			iceberg_t = self.repo.head.tree['iceberg']
		except Exception:
			pass
		
		if iceberg_t != None:
			return True
		return False
		
	
	def __getattr__(self, name):
		return getattr(self.repo, name)
		
	
		

class GitCollection(object):
	"""
	Hold a collection of instances of GIT repositories
	"""
	
	def __init__(self, prefix=None):
		"""
		prefix will help filter repos that you want to serve
		"""
		self.repos_= {}
		entries = os.listdir(GIT_ROOT)
		for d in entries:
			if prefix != None:
				pd = d.split('.')[0]
				if pd != prefix:
					continue
				
			name = os.path.join(GIT_ROOT,d)
			if os.path.isdir(name):
				try:
					repo = None
					try:
						repo = GitRepository(name)
						head = repo.head.commit_time
					except Exception as e:
						# print('Can not create a repo off [%s]'%name)
						# print('\t %s'%e)
						repo = None
					if repo != None:
						slug = d.rstrip('.git')
						self.repos_[slug] = repo
						
				except Exception as e:
					print 'ERROR (root): %s'%e
			
		# If we sort on __init__ we have to sort less often
		self.repos_ = OrderedDict(sorted(self.repos_.iteritems(), key=lambda r: r[1].head.commit_time, reverse=True))
				
	def get_names(self):
		return self.repos_.keys()
		
	def get_all(self):
		return self.repos_
	
	def __getattr__(self, name):
		if name in self.repos_:
			return self.repos_[name]
		else:
			raise AttributeError("GitCollection has no repository %s \n%s" % (name,self.repos_))
		
	# 3.4.6. Emulating container types <http://docs.python.org/reference/datamodel.html#emulating-container-types>
	# mainly by exposing "read-only" self.repos_'s methods 
	
	def __len__(self):
		return count(self.repos_)
		
	def __getitem__(self, key):
		return self.repos_[key]
		
	def __iter__(self):
		return self.repos_.__iter__()
		
	def __contains__(self, item):
		return self.repos_.__contains__(item)
		