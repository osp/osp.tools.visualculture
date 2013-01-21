all:
	git push
	ssh -t osp@ospwork.constantvzw.org 'cd /home/osp/apps/osp.tools.visualculture/; source /home/osp/apps/osp.tools.visualculture/venv/bin/activate; python /home/osp/apps/osp.tools.visualculture/vc_django/manage.py collectstatic --noinput; git pull; sudo /etc/init.d/apache2 restart'
