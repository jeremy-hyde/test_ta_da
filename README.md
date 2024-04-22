# Test Ta-Da

Suppositions:
- There is only one author so only one table to store blog articles
- I use the simplest database for this project: SQLite
- No index or other constraints on the article table
- The article read route has no parameters limit/skip
- The logger middleware writes in the console

## Start

### Install from poetry (Dev)
Download the project then:
```shell
poetry install
```

Activate the virtualenv with:
```shell
poetry shell
```

Run the server
```shell
python test_ta_da
```

### Install from wheel
Download the wheel available as release
```shell
python -m pip install {wheel_path}
```

Run the package
```shell
python -m test_ta_da
```

### Build package
```shell
poetry build
```

### Run Test
#### Pytest
```shell
pytest -vv --cov=test_ta_da
```

#### Schemathesis
```shell
st run --checks all http://127.0.0.1:8000/openapi.json --experimental=openapi-3.1
```

### Dev Tools
Lint check:
```shell
ruff check --fix
```

Format:
```shell
ruff format
```

Type Checker:
```shell
mypy test_ta_da
```

## Infos

### Environment

The project use:  
**Pyenv** to set the python version (see file .python-version).  
**Poetry** as environment/package/library management.  
**schemathesis** as an api fuzzer and an openapi specification checker  
**ruff** as formatter and linter  
**mypy** as a type checker  


### Improvements

- Make that the database is not drop between test but the changes are rollback
- Add a version prefix to the api
- Use Alembic for versioning of the database migration
- Use dotenv to set environments variables
- Load testing using locust
- Make stricter rules from ruff and mypy
- The schema Article can have each of its field empty. We might want to change that
