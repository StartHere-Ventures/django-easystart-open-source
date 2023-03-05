# django-easystart

Build the containers
```shell
docker-compose -f docker-compose.yml build
```

Launch the dev environment
````shell
docker-compose -f docker-compose.yml up
````

Generate routes file
````shell
docker-compose -f docker-compose.yml exec applocal python manage.py dump_routes_resolver --format=default --output=static/js/routes/resolver.js
````

Generate translations file
````shell
docker-compose -f docker-compose.yml exec applocal python manage.py compilemessages
docker-compose -f docker-compose.yml exec applocal python manage.py generate_i18n_js static/js/translation
````

Load fixtures
````shell
docker-compose -f docker-compose.yml exec applocal python manage.py loaddata fixtures/*.json
````

Open a new terminal to build the frontend on watch mode
````shell
docker-compose -f docker-compose.yml exec applocal npm install
docker-compose -f docker-compose.yml exec applocal npm run tailwind
docker-compose -f docker-compose.yml exec applocal npm run start
````

Open your browser at http://localhost:8000

## How to run tests
To tun the test using the pytest suite
````shell
docker-compose -f docker-compose.yml exec applocal pytest --disable-warnings
````

To get test coverage report:
````shell
docker-compose -f docker-compose.yml exec applocal pytest -p no:warnings --cov=.
````

## Code Quality - Python
For code quality checks and fixes you can use make to run AIO command

To ckeck for any errors just run:
```shell
make checkpython
```

To fix any errors just run:
```shell
make fixpython
```

OPCIONAL: you can run each test independently:

We use flake8 to source code linting. To ckeck for any errors just run:
```shell
docker-compose -f docker-compose.yml run --rm applocal flake8 .
```

We use black for code formatting. To check, view proposed changes and to apply them, run the following commands: 
```shell
docker-compose -f docker-compose.yml run --rm applocal black . --check
docker-compose -f docker-compose.yml run --rm applocal black . --diff 
docker-compose -f docker-compose.yml run --rm applocal black .
```

We use isort for sorting import statements. To check, view proposed changes and to apply them, run the following commands: 
```shell
docker-compose -f docker-compose.yml run --rm applocal isort . --check-only
docker-compose -f docker-compose.yml run --rm applocal isort . --diff
docker-compose -f docker-compose.yml run --rm applocal isort .
```

Before committing code to the repository, check for errors using the commands below and fix them if any:
```shell
docker-compose -f docker-compose.yml run --rm applocal flake8 .
docker-compose -f docker-compose.yml run --rm applocal black . --diff 
docker-compose -f docker-compose.yml run --rm applocal isort . --check-only
```

## Code Quality - Javascript / VueJS
For code quality checks and fixes you can use make to run AIO command

To ckeck for any errors just run:
```shell
make checkjs
```

To fix any errors just run:
```shell
make fixjs
```

OPCIONAL: you can run each test independently:
We use eslint to lint javascript code. To ckeck for any errors just run:
```shell
docker-compose -f docker-compose.yml run --rm applocal npm run lint
```

To fix errors just run: 
```shell
docker-compose -f docker-compose.yml run --rm applocal npm run lintfix
```

