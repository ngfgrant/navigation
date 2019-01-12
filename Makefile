define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

coverage-all:
		coverage erase
		coverage run --source navigation -m unittest
		coverage html
		coverage xml

coverage: coverage-all
		coverage report --show-missing
	    $(BROWSER) htmlcov/index.html

test:
	    pytest --junitxml=test-reports/junit.xml
	
lint:
	    flake8 .

acceptance-test:
	    behave acceptance-tests/

sonar:
	sonar-scanner \
				-Dsonar.projectKey=navigation \
				-Dsonar.sources=. \
				-Dsonar.host.url=http://127.0.0.1:9000 \
				-Dsonar.login=4256cabe75202d2ff2995309b8c748ce2f4ad2ba
