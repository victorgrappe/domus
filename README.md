
Domus
=====
Financing and forecasting of a real estate purchase in France


Run
---
```sh
pipenv run python3 main.py
```

Setup
-----

### env
```sh
cd .
source ".env"
```

### Pipenv
```sh
pipenv --rm
rm -f Pipfile Pipfile.lock
```
```sh
pipenv install --python "${O_PYTHON_VERSION}"
pipenv install "pandas==${O_PANDAS_VERSION}"
pipenv install "numpy-financial==${O_NPFINANCIAL_VERSION}"
```
```sh
pipenv check
pipenv graph
pipenv run python3 --version
cat Pipfile
```