# Mobile Bank System

## Project requirements

* docker >= 20.10.0
```docker --version```
* docker-compose >= 1.29.0
```docker-compose --version```
* python >= 3.10


# Development Environment Set Up

## Start project local
### Clone Project to your local environment
```bash
  git clone git@github.com:rGudavadze/mobile-bank-system.git
```

### Create virtual environment
```bash
  python -m venv <env-name>
```

### add env variables
```text
  create .env directory, copy files from .env-pattern dir and fill the
  variables with appropriate values.
```

### Install requirements
```bash
  make install_requirements
```

## Run project using docker-compose
#### Build and start containers
Build images and start containers. Migration command will be run during startup.
```bash
  make build_app_docker
  make run_app_docker
```

#### Working with running container
* When container is running
```bash
  docker-compose exec bank-api <your_command>
```
* Without running container
```bash
  docker-compose run --rm bank-api <your_command>
```

### Installation pre-commit

```bash
  make install_pre_commit
```

### Unit tests
Run tests
```bash
  make run_tests
```


## Project Structure

```bash
src/
    apps/
         app_name/
              models/
              serializers/
              views/
              urls/
              ... # other app modules
         ...      # all other apps will be placed here
    core/
         settings/
    utils/
          ...

docker-compose.yml
dockerfiles/
    Dockerfile
    ...
requirements.txt
```
