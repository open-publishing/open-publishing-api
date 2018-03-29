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
	PYTHONPATH="${PYTHONPATH}:/" python3 -m unittest discover -s test -p "*_test.py" -b

build:
	@python3 setup.py sdist --formats=gztar
	#@python3 setup.py egg_info

pypi:
	# python3 setup.py register -r pypi
	#@python3 setup.py sdist upload -r pypi
	echo "Upload to pypi disabled"

pylint:
	@pylint -j 8 --rcfile=.pylintrc open_publishing2 test/*.py *.py examples/*.py

pydocstyle:
	 @pydocstyle open_publishing2 test/*.py test/*.py *.py examples/*.py

coverage:
	py.test --cov-report html --cov open_publishing2 --verbose

.PHONY: test build
