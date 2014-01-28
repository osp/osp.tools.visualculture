all:
	ssh -t osp@37.34.55.224 'cd /home/osp/apps/osp.tools.visualculture/; source /home/osp/apps/venv/bin/activate; git pull readonly master; python /home/osp/apps/osp.tools.visualculture/visualculture/manage.py collectstatic --noinput; sudo supervisorctl restart visualculture'
