<h1 align="center">virtu-mall</h1>
<p align="center"><img width="180" src="./logo.png" alt="logo" /></p>
<p align="center">VirtuMall는 파이썬으로 작성한, 쇼핑몰 프로젝트 입니다.</p>
<p align="center">효율적이고 안정적인 API를 제공하여 사용자가 손쉽게 다양한 쇼핑  관련 작업을 수행할 수 있도록 하는 목적을 가지고 있습니다.</p>

[![GitHub Super-Linter](https://github.com/f-lab-edu/virtu-mall/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Getting started

### Overview

Name    | Version
--------|---------
Python  | 3.11
Django  | 4.2.7

### Installation

0. 애플리케이션 구동에 필요한 환경을 설정합니다.
- 필요 소프트웨어
    - Python version >= 3.11 (venv)
- .env.example 을 참조하여 .env 를 backend 프로젝트 루트에 생성합니다.

1. 프로젝트 종속성을 설치합니다.
```shell
# Project venv 가 활성화되어있어야 합니다.
(venv) $ pip install -r requirements/requirements.txt
(venv) $ python manage.py migrate
```

2. 어드민에서 필요한 추가 설정을 위해 관리자 계정 생성 후 서버를 실행합니다.
```shell
(venv) $ python manage.py createsuperuser
(venv) $ python manage.py runserver
```

## Developer guide

### Docker build

- TBD.

### Testing

- TBD.

### Linting
Name    | Version | Description
--------|---------|----------------
Black   | 23.11.0 | Formats Python code adhering to our style guidelines.
Isort   | 5.12.0  | Sorts imports alphabetically and automatically separates them into sections.
Flake8  | 6.1.0   | Checks for PEP 8 compliance and other coding standards.
