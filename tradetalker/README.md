## Backend development
### General notes
- The Python interpreter is using version 3.11.7.
- Please make sure to lint all Python code and fix any issues by running the `lint.sh` script in the `api` directory before committing. This will install `pipenv` and create a `pipenv` virtual environment where the required packages will be installed. Then, it will run `black`, `pylint`, `ruff` and `pyright`. If no errors appear, the code is okay.

### Installing packages
1. Make sure you have `pipenv` installed (if not, run `pip install pipenv`)
2. From the project root, navigate to the `api` directory (this is where the backend code will be located)
```
cd api
```
3. Install all dependencies:
```python
pipenv install --dev
```
4. Activate the shell:
```python
pipenv shell
```
5. Install your desired package(s) (add `--dev` if it's for developer use only):
```python
pipenv install <package> [--dev]
```
6. Update the lockfile when done:
```python
pipenv lock
```
7. Exit the virtual environment:
```python
exit
```

## Frontend development

- To install a Node package, run `npm install <package>`. Make sure that `pnpm-lock.yaml` is kept up to date by running `pnpm install` after a package installation.
- Please make sure to lint all JS/TS code and fix any issues by running `npm run lint` before committing.
