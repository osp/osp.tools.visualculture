all:
	echo "UPDATING OSP.CONSTANTVZW.ORG"
	ssh -t osp@37.34.55.224 'cd /home/osp/apps/osp.tools.visualculture/; source /home/osp/apps/venv/bin/activate; git pull readonly master; python /home/osp/apps/osp.tools.visualculture/visualculture/manage.py collectstatic --noinput; sudo supervisorctl restart visualculture'
	echo "UPDATING OSPWORK.CONSTANTVZW.ORG"
	ssh -t osp@ospwork.constantvzw.org 'cd /home/osp/apps/osp.tools.visualculture/; source /home/osp/apps/osp.tools.visualculture/venv/bin/activate; python /home/osp/apps/osp.tools.visualculture/visualculture/manage.py collectstatic --noinput; git pull; sudo /etc/init.d/apache2 restart'

