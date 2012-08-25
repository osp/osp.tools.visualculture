
import os
import errno

from visual_culture.readers import Reader

from celery import task

def ensure_dir(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise exception

@task.task()	
def read_blob(cache_root, blob_info, blob_data):
	r = Reader()
	ret = r.read_blob(blob_info, blob_data)
	ensure_dir(os.path.join(cache_root, blob_info['repo_name']))
	f = open(os.path.join(cache_root, blob_info['repo_name'], blob_info['commit']), 'wb')
	f.write(ret['data'])
	f.close()
	return ret