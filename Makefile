# Options for ENV are dev (default) or prod
ENV = dev
ROOTDIR := ${CURDIR}

checkall: checkpython checkjs

fixall: fixpython fixjs

checkpython: checkpython$(ENV)
 
checkpythondev:
	####### Running checks for python code quality in $(ENV) enviroment #######
	#
	# Running flake8 #
	docker-compose -f docker-compose.yml run --rm applocal flake8 .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose.yml run --rm applocal black . --diff
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose.yml run --rm applocal isort . --check-only
	#
	###########################################################################

checkpythonprod:
	####### Running checks for python code quality in $(ENV) enviroment #######
	#
	# Running flake8 #
	docker-compose -f docker-compose-prod.yml run --rm app flake8 .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose-prod.yml run --rm app black . --diff
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose-prod.yml run --rm app isort . --check-only
	#
	###########################################################################

fixpython: fixpython$(ENV)

fixpythondev:
	####### Running fixes for python code quality in $(ENV) enviroment #######
	#
	# Running flake8 #
	docker-compose -f docker-compose.yml run --rm applocal flake8 .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose.yml run --rm applocal black .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose.yml run --rm applocal isort .
	#
	###########################################################################

fixpythonprod:
	####### Running fixes for python code quality in $(ENV) enviroment ########
	#
	# Running flake8 #
	docker-compose -f docker-compose-prod.yml run --rm app flake8 .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose-prod.yml run --rm app black .
	#
	###########################################################################
	#
	# Running black #
	docker-compose -f docker-compose-prod.yml run --rm app isort .
	#
	###########################################################################


checkjs: checkjs$(ENV)
 
checkjsdev:
	######### Running checks for js code quality in $(ENV) enviroment #########
	#
	# Running lint #
	docker-compose -f docker-compose.yml run --rm applocal npm run lint
	#
	###########################################################################

checkjsprod:
	######### Running checks for js code quality in $(ENV) enviroment #########
	#
	# Running lint #
	docker-compose -f docker-compose-prod.yml run --rm app npm run lint
	#
	###########################################################################


fixjs: checkjs$(ENV)
 
fixjsdev:
	######### Running fixes for js code quality in $(ENV) enviroment ##########
	#
	# Running lintfix #
	docker-compose -f docker-compose.yml run --rm applocal npm run lintfix
	#
	###########################################################################

fixjsprod:
	######### Running fixes for js code quality in $(ENV) enviroment ##########
	#
	# Running lilintfixnt #
	docker-compose -f docker-compose-prod.yml run --rm app npm run lintfix
	#
	###########################################################################

runtests:
	######### Used for running tests in a standalone container without dependencies ##########
	#
	# Running tests on app container without dependencies                                    #
	docker-compose run --entrypoint="" --no-deps --rm applocal pytest
	##########################################################################################

runtestsci:
	######### Used for running tests to run test in parallel distributing them  across cpus ########
	#
	# Running tests on app container without dependencies                                          #
	docker-compose run --entrypoint="" --no-deps --rm applocal pytest -n auto
	################################################################################################