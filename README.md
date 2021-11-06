# Roosevelt Park's Alerting System

[![CircleCI](https://img.shields.io/circleci/build/github/code-for-good-wm/rooseveltparkna-alerts)](https://circleci.com/gh/code-for-good-wm/rooseveltparkna-alerts)
[![Coveralls](https://img.shields.io/coveralls/github/code-for-good-wm/rooseveltparkna-alerts)](https://coveralls.io/github/code-for-good-wm/rooseveltparkna-alerts)

This project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-django](https://github.com/jacebrowning/template-django).

# Setup

## Requirements

The following must be installed on your system:

- Make
- Python
- Poetry
- PostgreSQL

To confirm the correct versions are installed:

```
$ make doctor
```

## Setup

Create a database:

```
$ createdb rpna_dev
```

Install project dependencies:

```
$ make install
```

Run migrations and generate test data:

```
$ make data
```

## Development

Run the application and recompile static files:

```
$ make run
```

See the [contributor guide](CONTRIBUTING.md) for additional details.
