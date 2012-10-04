"""
vc_cache.utils
"""

import os
import errno

def ensure_dir(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise exception

def hash_options(options):
	opt_a = []
	for k in options:
		opt_a.append('%s..%s'%(k, options[k].replace('/','_')))
	h = '/'.join(sorted(opt_a));
	return h