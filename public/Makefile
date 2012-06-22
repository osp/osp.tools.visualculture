BOOTSTRAP_LESS = ./less/bootstrap.less
BOOTSTRAP_RESPONSIVE_LESS = ./less/responsive.less
LESS_COMPRESSOR ?= `which lessc`
WATCHR ?= `which watchr`

# BUILD SIMPLE BOOTSTRAP DIRECTORY
# lessc & uglifyjs are required
#

bootstrap:
	lessc ${BOOTSTRAP_LESS} > css/osp.main.css
	lessc --compress ${BOOTSTRAP_LESS} > css/osp.main.min.css
	lessc ${BOOTSTRAP_RESPONSIVE_LESS} > css/osp.responsive.css
	lessc --compress ${BOOTSTRAP_RESPONSIVE_LESS} > css/osp.responsive.min.css
	cat js/bootstrap-transition.js js/bootstrap-alert.js js/bootstrap-button.js js/bootstrap-carousel.js js/bootstrap-collapse.js js/bootstrap-dropdown.js js/bootstrap-modal.js js/bootstrap-tooltip.js js/bootstrap-popover.js js/bootstrap-scrollspy.js js/bootstrap-tab.js js/bootstrap-typeahead.js > js/bootstrap.js
	uglifyjs -nc js/bootstrap.js > js/bootstrap.min.js

#
# WATCH LESS FILES
#

watch:
	echo "Watching less files..."; \
	watchr -e "watch('less/.*\.less') { system 'make' }"


.PHONY: dist docs watch gh-pages
