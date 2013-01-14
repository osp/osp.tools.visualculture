
import os

from visual_culture.readers import Reader

from celery import task

from vc_cache import utils 

import time

@task.task()    
def read_blob(cache_root, blob_info, options):
    print('[%s] Starting read_blob task'%(time.asctime(),))
    r = Reader()
    ret = r.read_blob(blob_info, options)
    print('R %s'%cache_root)
    print('I %s'% blob_info['repo_name'])
    print('H %s'%utils.hash_options(options))
    cpath = os.path.join(cache_root, blob_info['repo_name'], utils.hash_options(options))
    utils.ensure_dir(cpath)
    f = open(os.path.join(cpath, blob_info['commit']), 'wb')
    f.write(ret['data'])
    f.close()
    return ret