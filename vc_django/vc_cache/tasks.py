
import os
import errno

from visual_culture.readers import Reader

from celery import task

from vc_cache import utils 



@task.task()	
def read_blob(cache_root, blob_info, blob_data, options):
	r = Reader()
	ret = r.read_blob(blob_info, blob_data, options)
	print('R%s'%cache_root)
	print('I%s'% blob_info['repo_name'])
	print('H%s'%utils.hash_options(options))
	cpath = os.path.join(cache_root, blob_info['repo_name'], utils.hash_options(options))
	utils.ensure_dir(cpath)
	f = open(os.path.join(cpath, blob_info['commit']), 'wb')
	f.write(ret['data'])
	f.close()
	return ret