# python-app-boilerplate
Python application boilerplate. This boilerplate may be used for scripts, CLIs, or GUI or non GUI services. 

## Requirements

- Git 2.47.0+
- Python 3.12.6+
- uv 0.6.3+
- Docker 27.4.0+ [optional]

## Problems

- No synchronization between uv-dynamic-versioning project version and docker image built. Current approach uses fallback version
```
[tool.uv-dynamic-versioning]
fallback-version = "0.0.0" 
```
- No tool for enforcing creation of pre-release branches to have a `*/*` format like `feat/some-feature`. Current approach is giving coding guidelines

## Project structure
```
project/
├── .benchmarks/                # Benchmarks reports [pytest.ini --benchmark-autosave argument]
├── .github/workflows           # Github Actions workflows 
├── docker/                     # Dockerfiles
├── docs/                       # Documentation template
├── htmlcov/                    # Coverage reports   [pytest.ini --cov-report=html]
├── profiling/                  # Profiling script
├── site/                       # Generated documentation
├── src/                        # Code source 
│   └── python_app_boilerplate/ # Name of project
│       └──...                  # Python files of project   
├── test/                       # Test files 
│   ├── benchmark/              # Benchmark tests
│   ├── unit/                   # Unit tests
│   └── [conftest.py]           # Setup tests
├── .coveragerc                 # Coverage setup     [pytest.ini --cov-config=.coveragerc]
├── .gitignore                  # Git ignored files
├── .pre-commit-config.yaml     # Pre-commit setup
├── .python-version             # Project python version
├── .ruff.toml                  # Ruff setup
├── LICENSE                     # Project License
├── mkdocs.yaml                 # Mkdocs setup
├── mypy.ini                    # Mypy setup
├── pyproject.toml              # Project setup
├── pytest.ini                  # Pytest setup
├── README.md                   # README.md
└── uv.lock                     # Dependencies declaration
```

## How to use

### Development

1. Clone the repository in the pwd of your project.
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Install the project
```bash
uv sync --dev
```
3. Install pre-commit hooks
```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```
4. Run the project
```bash
uv run app
```
5. Change instances of `python_app_boilerplate_25_d` to your project name in the following files and folders:
- pyproject.toml: project name and app script.
- README.md: Project structure, deployment.
- src/python_app_boilerplate_25_d: Folder name.
- *.py: Top path comment.
- docs/reference/api.md: Reference to python_app_boilerplate.

6. Commits should follow the [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) guideline for semantic-release to auto generate tags and versions that follow [semantic-versioning](https://semver.org/) in the CI/CD pipeline. Commitizen can be used to generate conventional commits
```bash
uv run cz commit
```

### Profiling

1. Clone the repository in the pwd of your project.
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Install the project
```bash
uv sync --dev
```
3. Check the `profiling/profiler.py` script and replace the function under the comment to profile.
```py
# Place function to profile here
```  
4. Run the profiling script from the root of the project.
```bash
uv run profiling/profiler.py
```
5. Check the reports on profiling/reports.

### Documentation

1. Clone the repository in the pwd of your project.
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Install the project docs dependencies
```bash
uv sync --group docs
```
3. Build the documentation
```bash
uv run mkdocs build
```
4. Serve the documentation locally or use built documentation in the `site/` folder to deploy it on a web server.
```bash
uv run mkdocs serve
```

### Committing, Formatting, Linting, Type Checking, and Testing

Before committing changes, make sure to run the commit check, formatter, linter, type checker, and tests.

- Pre-commit hooks will run the commit check, formatter, linter, and type checker before committing changes. To run the pre-commit hooks manually, use the following command:
```bash
pre-commit run --all-files
```
- (Optional) Run the commit check for [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) to test validate commit
```bash
uv run cz check --message commit
```
- (Optional) Run the linter and formatter
```bash
uv run ruff format
uv run ruff check --fix
```
- (Optional) Run the type checker
```bash
uv run mypy .
```
- (Optional) Run the tests and coverage
```bash
uv run pytest --cov
```

## Deployment

- Scripts may not need a deployment or packaging
- CLIs, GUIs/non-GUI services could be deployed from a docker image or built, packaged and published to PyPI or Github Release
- GUIs application may need an specific command in Windows. [reference](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
```
[project.gui-scripts]
app-gui = "python_app_boilerplate_25_d.main:main_gui"
```

### Automatic release

1. Clone the repository
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```

2. Set up the PyPI and TestPyPi tokens in Github secrets used by `.github/workflows/release.yml` as environmental variables

3. Push to the `main` for releases, and to a `*/*` format like branch for pre-releases 

4. Once commited, the `.github/workflows/release.yml` workflow runs. `semantic-release` generates a git tag based on the `.releaserc.json`, and it pushes to github release. Finally, the running workflow publishes to PyPI or TestPyPi with the updated dynamic version from `semantic-release` using `uv build` and `uv publish`

| release type          | prerelease    | release   |
| --------              | -------       |-------    |
| Release type          | \*/\*         | main      |
| Versioning            | v1.0.0-rc.1   | v1.0.0    |
| Git Tag               | v1.0.0-rc.1   | v1.0.0    |
| Git Releases          | pre-release   | release   |
| Index Publishing      | testPyPi      | pyPi      |

### Manual TestPyPi/PyPi

1. Clone the repository
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Build the project
```bash
uv build
```
3. Publish to an index using the `--token` flag with a token generated from PyPi or TestPyPi. Use `--index testpypi` flag to publish to TestPyPi as specified in the `pyproject.toml`, by default it publishes to PyPi.
```bash
uv publish
```

### Docker

1. Clone the repository
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Build the Docker image from the root of the project
```bash
docker build . --file docker/app.Dockerfile --tag python-app
```
3. Run the Docker container
```bash
docker run python-app
```

### Docker Compose

1. Clone the repository
```bash
git clone git@github.com:25-d/python-app-boilerplate .
```
2. Build the Docker image from the root of the project. Pass the `--build` flag to rebuild the image if there are changes in the Dockerfile or the application code.
```bash
docker-compose --file docker/docker-compose.yml up --detach 
```
