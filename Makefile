all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "pypi           -- upload package to pypi"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "pydocstyle      -- run pydocstyle tests"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""

test:
	nosetests
test-docker: check_env_devname
	-docker rm open-publishing-tests-runner
	docker build . -t open-publishing-tests
	docker run -e APIHOST=api.$(NG_DEVNAME).dev.openpublishing.com --name=open-publishing-tests-runner open-publishing-tests --with-xunit --xunit-file=/results.xml
	docker cp open-publishing-tests-runner:/results.xml .
	docker rm open-publishing-tests-runner

check_env_devname:
ifndef NG_DEVNAME
        $(error NG_DEVNAME not set.)
endif

build:
	@python3 setup.py sdist --formats=gztar
	#@python3 setup.py egg_info

pypi:
	# python3 setup.py register -r pypi
	# @python3 setup.py sdist upload -r pypi
	@python3 setup.py sdist upload -r local
	#echo "Upload to pypi disabled"

pylint:
	@pylint -j 8 --rcfile=.pylintrc open_publishing2 test/*.py *.py examples/*.py

pydocstyle:
	 @pydocstyle open_publishing2 test/*.py test/*.py *.py examples/*.py

coverage:
	py.test --cov-report html --cov open_publishing2 --verbose

.PHONY: test build
