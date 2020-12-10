# Tick Track

## Description

Nothing but a time time tracker, to understand where you spend your ticks every day, because every tick counts.

## Requirements

- python >= 3.6
- pipenv
- docker
- docker-compose

## Stack

- API: Sanic
- ORM: Peewee

## Usage

### Installation

#### pipenv

```sh
pip3 install pipenv
```

#### Python requirements

```make
make install-py
```

### Runing the server

#### Apply database's migrations

```make
make migrate
```

#### Run produtction app

```make
make run-prod
```

#### Run development app

```make
make run-dev
```

## Not Implemented yet

- Idle user time for windows and macOs
