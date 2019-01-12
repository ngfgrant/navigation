coverage-all:
		coverage erase
		coverage run --source navigation -m unittest
		coverage xml

coverage: coverage-all
		coverage report --show-missing

test:
	    pytest --junitxml=test-reports/junit.xml
	
lint:
	    flake8 .

acceptance-test:
	    behave acceptance-tests/

sonar:
		sonar-scanner \
				  -Dsonar.projectKey=ngfgrant_navigation \
				  -Dsonar.organization=ngfgrant-github \
				  -Dsonar.sources=. \
				  -Dsonar.host.url=https://sonarcloud.io \
				  -Dsonar.login=${sonar_login}
