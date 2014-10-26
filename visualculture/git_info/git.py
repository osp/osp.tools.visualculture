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
        
        self.repo_fullname = os.path.basename(os.path.normpath(fname))
        if self.repo_fullname.endswith('.git'):
            self.repo_fullname = self.repo_fullname[:-4]
        self.repo_parts = self.repo_fullname.split('.')
        if len(self.repo_parts) > 2:
            self.repo_prefix = self.repo_parts[0]
            self.repo_category = self.repo_parts[1]
            self.repo_name = '.'.join(self.repo_parts[2:])
        else:
            self.repo_prefix = ''
            self.repo_category = ''
            self.repo_name = self.repo_fullname
    
    def __getattr__(self, name):
        return getattr(self.repo, name)
        
    def __getitem__(self, key):
        return self.repo[key]
        
        
class GitCollection(object):
    """
    Hold a collection of instances of GIT repositories
    """
    
    def __init__(self, prefix=None):
        """
        prefix will help filter repos that you want to serve
        """
        self.prefix = prefix
        self.repos_= {}
        self.lazy_loaded_ = False 
        
    def reset(self):
        self.repos_= {}
        self.lazy_loaded_ = False 
        
    def watch(self, repo_path, is_bare = True):
        pass
        
    def lazy_load_(self, name):
        if not self.lazy_loaded_ and self.repos_:
            #print('%s %s %s'%(name,self.lazy_loaded_, len(self.repos_)))
            return
        
        if name in self.repos_:
            return
        
        base_path = os.path.join(GIT_ROOT, name)
        bare_path = os.path.join(GIT_ROOT, '.'.join([name,'git']))
        for path in [base_path, bare_path]:
            try:
                repo = None
                try:
                    repo = GitRepository(path)
                except Exception as e:
                    #print('Unable to instanciate a GitRepo for: %s'%path)
                    repo = None
                if repo != None:
                    self.repos_[name] = repo
                    self.watch(path, repo.is_bare)
                    break
                    
            except Exception as e:
                print 'ERROR (lazy_load_): %s'%e
        self.lazy_loaded_ = True 
        
            
    def load_all_(self):
        if self.lazy_loaded_:
            self.repos_={}
            self.lazy_loaded_ = False 
        else:
            if self.repos_:
                return
                
        entries = os.listdir(GIT_ROOT)
        for d in entries:
            if self.prefix != None:
                pd = d.split('.')[0]
                if pd != self.prefix:
                    continue
                
            name = os.path.join(GIT_ROOT,d)
            if os.path.isdir(name):
                try:
                    repo = None
                    try:
                        repo = GitRepository(name)
                        head = repo.head.get_object().commit_time
                    except Exception as e:
                        # print('Can not create a repo off [%s]'%name)
                        # print('\t %s'%e)
                        repo = None
                    if repo != None:
                        if d.endswith('git'):
                            slug = d[:-4]
                        else:
                            slug = d
                        self.repos_[slug] = repo
                        self.watch(name, repo.is_bare)
                        
                except Exception as e:
                    print 'ERROR (root): %s'%e
            
        # If we sort on __init__ we have to sort less often
        self.repos_ = OrderedDict(sorted(self.repos_.iteritems(), key=lambda r: r[1].head.get_object().commit_time, reverse=True))
        
    def get_names(self):
        self.load_all_()
        return self.repos_.keys()
        
    def get_all(self):
        self.load_all_()
        return self.repos_
    
    def __getattr__(self, name):
        self.lazy_load_(name)
        if name in self.repos_:
            return self.repos_[name]
        else:
            raise AttributeError("GitCollection has no repository %s \n%s" % (name,self.repos_))
            
        
    # 3.4.6. Emulating container types <http://docs.python.org/reference/datamodel.html#emulating-container-types>
    # mainly by exposing "read-only" self.repos_'s methods 
    
    def __len__(self):
        self.load_all_()
        return count(self.repos_)
        
    def __getitem__(self, key):
        self.lazy_load_(key)
        return self.repos_[key]
        
    def __iter__(self):
        self.load_all_()
        return self.repos_.__iter__()
        
    def __contains__(self, item):
        self.lazy_load_(name)
        return self.repos_.__contains__(item)
        