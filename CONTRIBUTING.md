# For Contributors

## Setup

### Requirements

* Make:
    * Windows: http://mingw.org/download/installer
    * Mac: http://developer.apple.com/xcode
    * Linux: http://www.gnu.org/software/make
* Python: `$ pyenv install` or `$ asdf install`
* Poetry: https://python-poetry.org/docs/#installation
* PostgreSQL: `$ brew install postgres`
    - If using Ubuntu on WSL2 and keeping the default socket connection, change the postgres' user's authentication method to `trust` instead of `peer` so you can run commands with your Ubuntu login. Configuration can be found in `/etc/postgresql/{version}/main/pg_hba.conf`. Be sure to restart the postgres service after saving changes. This also requires changing `config\settings\local.py` to use `"USER": "postgres"` instead of `"HOST": "127.0.0.1"`
* direnv: https://direnv.net/

To confirm these system dependencies are configured correctly:

```
$ make doctor
```

### Installation

Install project dependencies into a virtual environment:

```
$ make install
```

### Data

To automatically create test accounts, update `.envrc` with your own information and run `direnv allow`. Then, generate new seed data for local development:

```
$ make data
```

## Development Tasks

### Testing

Manually run the tests:

```
$ make test
```

or keep them running on change:

```
$ make watch
```

> In order to have OS X notifications, `brew install terminal-notifier`.

### Static Analysis

Run linters and static analyzers:

```
$ make check
```

## Continuous Integration

The CI server will report overall build status:

```
$ make ci
```
