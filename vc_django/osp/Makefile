all:
	git push
	ssh -t osp@ospwork.constantvzw.org 'cd /home/osp/apps/osp.tools.visualculture/; git pull; sudo /etc/init.d/apache2 restart'
