<h1 align="center">virtu-mall</h1>
<p align="center"><img width="180" src="./assets/logo.png" alt="logo" /></p>
<p align="center">VirtuMall는 파이썬으로 작성한, 쇼핑몰 프로젝트 입니다.</p>
<p align="center">효율적이고 안정적인 API를 제공하여 사용자가 손쉽게 다양한 쇼핑  관련 작업을 수행할 수 있도록 하는 목적을 가지고 있습니다.</p>

[![GitHub Super-Linter](https://github.com/f-lab-edu/virtu-mall/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Getting started

### Overview

Name    | Version
--------|---------
Python  | 3.11
Django  | 4.2.7

## Developer guide

### Docker build

0. 애플리케이션 구동에 필요한 환경을 설정합니다.
- 필요 소프트웨어
    - Docker >= 24.0.6
- .env.example 을 참조하여 .env 를 backend 프로젝트 루트에 생성합니다.

1. build docker image
```shell
docker build -f ./docker/Dockerfile -t aohus/virtu-mall .
```

2. run docker container
```shell
docker-compose -f docker-compose-local.yml up
```

컨테이너가 실행되면, 브라우저에서 `http://0.0.0.0:8000`을 통해 접근할 수 있습니다.

cf)
`Exception: Can not find valid pkg-config name.
Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually`
위와 같은 에러가 발생한다면, 아래 패키치 설치를 통해 해결하세요. 

- macOS
```shell
brew install mysql pkg-config
```

- Linux
```shell
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```


### Testing

- TBD.

### Linting
Name    | Version | Description
--------|---------|----------------
Black   | 23.12.0 | Formats Python code adhering to our style guidelines.
Isort   | 5.13.1  | Sorts imports alphabetically and automatically separates them into sections.
Flake8  | 6.1.0   | Checks for PEP 8 compliance and other coding standards.
mypy    | 1.7.1   | Static type checker for Python.
