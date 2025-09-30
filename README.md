# fabric-analytics

Pre-requisites: python3.10
For Fabric Analytics Main Web Server, before running the web server::
    1. Create a new virtual environment: python3.10 -m venv venv
    2. activate the virtual environment: source venv/bin/activate
    3. Install requirements: pip install -r requirements.txt
    4. Set path: export PYTHONPATH=<absolute/path/to/fabric-analytics>


### Pre-commit hooks

Git hook scripts are useful for identifying simple issues before submission to code review. It runs every commit to automatically point out issues in code such as missing semicolons, trailing whitespace, and debug statements. By pointing these issues out before code review, this allows a code reviewer to focus on the architecture of a change while not wasting time with trivial style nitpicks.

#### Installation

Before you can run hooks, you need to have the pre-commit package manager installed.

Using pip:

```
pip install pre-commit
```

Using homebrew

```
brew install pre-commit
```

Run `pre-commit install` to install pre-commit into your git hooks. pre-commit will now run on every commit. Every time you clone a project using pre-commit running `pre-commit install` should always be the first thing you do.

### Commitzen

Commitizen is release management tool designed for teams.

#### Installation

Using pip:

```
pip install -U commitizen
```

Using homebrew

```
brew install commitizen
```

### Usage

Most of the time this is the only command you'll run:

```
cz bump
```

On top of that, you must use commitizen to assist you with the creation of commits. We will follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to ensure the standard commit messages across the team:

```
git cz commit
```

First, commit the code then run bump command. We will use [Semantic Versioning](https://semver.org) to maintain the changelog


# analytics_engine

### Set-up

```
python3.10 -m venv .venv
source activate .venv/bin/activate

pip install --upgrade pip

pip install -e .
```


## Backend Code compilation:
```
make compile
```

## Run Using (development)

Docker:
```
docker compose up --build
```

Command line:
```
gunicorn -k eventlet -w 1 --bind 0.0.0.0:5000 --log-config log_config.conf socket_server:app
```


# Productionization

## Build Image:
Note: create .env file inside fabric_analytics_frontend folder before building
```
make build-image TAG=<specify tag here>
```

## Push Image to Dockerhub:
```
make push-image TAG=<specify tag here> TOKEN_BE=<backend dockerhub access token> TOKEN_FE=<frontend dockerhub access token>
```
Note: Write access is required for the token.

## Running local(already downloaded) Image:
```
make run TAG=<specify tag here>
```

## Pull & Run Image:
```
make pull-run TAG=<specify tag here> TOKEN_BE=<backend dockerhub access token> TOKEN_FE=<frontend dockerhub access token>
```
Note: Read-only access is required for the token.
