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

## Deploy to producition environment

1. Add `.env` file to fill variable in yaml file
2. Add `.envs/.production/.dajngo` & `.envs/.production/.postgres` & `.envs/.production/.nginx` file in root folder

```bash
docker-compose -f production.yml up -d
```

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the tags on this repository.

## Authors

* Jeff SH Wang (Backend)
* Leo Tu (Frontend)
