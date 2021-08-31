# Develop Requirement System

One system record software's development spec, flow, member, etc.

## Prerequisites

* Python 3.7.x above

* Ubuntu 16.04 LTS / 18.04LTS

## Install development environment

Use **`pipenv`** to install all require python package

```bash
pipenv isntall
```

## Development Process

* Check upstream package change

    ```bash
    pipenv update --outdated
    ```

* Update all package

    ```bash
    pipenv update
    ```

* Update specific package

    ```bash
    pipenv update <pkg>
    ```

## Before Production

* Generate new `requirements/local.txt`

    ```bash
    pipenv lock -r --dev > requirements/local.txt
    ```

* Generate new `requirements/production.txt`

    ```bash
    pipenv lock -r > requirements/production.txt
    ```

## Deploy to production environment

* Clone from remote repository and change to develop branch

    ```bash
    git clone http://10.32.36.106:10080/TQMS/a32_develop_requirement_system/develop_requirement_dev
    cd develop_requirement_dev
    git checkout develop
    ```

* Setup all config in the folder (`.envs\.production\`) and `.env` file

* Build docker image

    ```bash
    docker-compose -f production.yml --compatibility build
    ```

* Migrate database

    ```bash
    docker-compose -f production.yml run --rm django python manage.py makemigrations
    docker-compose -f production.yml run --rm django python manage.py migrate
    ```

* Deploy service

    ```bash
    docker-compose -f production.yml --compatibility up -d --scale django=5
    ```

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

## Authors

* Jeff SH Wang (Backend)
* Leo Tu (Frontend)
