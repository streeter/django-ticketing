## About

An implementation of a Django model that returns tickets, as described
in the [Flickr blog post][flickr]. Requires Python 3.11 or higher and Django 5.2
or higher. Ticket generation supports MySQL 8.4 or higher and SQLite.

## Installation

I uploaded it to [PyPi][pypi], so you can grab it there if you'd like with

```
pip install django-ticketing
```

or install it with pip using the git address:

```
pip install git+git@github.com:streeter/django-ticketing.git
```

Then add `ticketing` to your `INSTALLED_APPS`.

## Usage

To use this, you can either use the model interface, or just the shortcut
function defined in `ticketing.models`. That usage looks like this:

```python
# Import the function
from ticketing.models import get_ticket

# Go get yourself a ticket
ticket = get_ticket()
# Boom. That just happened
```

Create the sequence tables before requesting tickets. The app generates its
models from your settings and does not ship migrations; use Django's
`migrate --run-syncdb` to create tables for this unmigrated app.

### Multiple Sequences

`django-ticketing` also supports multiple sequences, which allows to have
sequences of tickets that are independent. This means you could have a sequence
for users, a sequence for posts and a sequence for widgets. This is configured
through your Django settings configuration.

Simply define a setting called `TICKETING_SEQUENCES` with a tuple of sequence
names that have to be valid table names. This defaults to the tuple `('default',)`.
In addition, you can define the default sequence from which new tickets are
taken from with the setting `TICKETING_DEFAULT_SEQUENCE`, which defaults to
`'default'`.

Note that `TICKETING_DEFAULT_SEQUENCE` has to be a sequence name that is defined
inside of `TICKETING_SEQUENCES`, otherwise an exception will be raised
during setup.

So to have sequences for the above example, put the following lines in your
`settings.py`:

``` python
TICKETING_DEFAULT_SEQUENCE = "users"
TICKETING_SEQUENCES = (
    "users",
    "posts",
    "widgets",
)
```

Then, to get a ticket from a specific sequence, pass in the sequence name to
`get_ticket()`:

``` python
# Get yourself a user ticket
user_ticket = get_ticket("users")
# Get yourself another user ticket
user_ticket = get_ticket()
# Get yourself a posts ticket
post_ticket = get_ticket("posts")
```

Notice that the default sequence for `get_ticket()` is the value of the
`TICKETING_DEFAULT_SEQUENCE` configuration variable.

Also, after you change the value of `TICKETING_SEQUENCES`, be sure to re-run
`python manage.py migrate --run-syncdb` to create any new sequence tables.

### Other Configuration Options

`TICKETING_APP_LABEL`: This is used to specify the prefix for all the DB
tablenames. The default value is `'ticketing'`. Be sure you know what you are
doing when you change this.


## Testing

Install the development tools in a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Run the pytest suite against the current environment, or use Tox for the full
compatibility matrix and Ruff checks:

```bash
pytest
tox
```

Tox requires each Python interpreter in the matrix to be installed. Missing
interpreters fail the run so coverage cannot silently disappear. To run just
one environment or one test:

```bash
tox -e py315-django61
tox -e py315-django61 -- -k test_get_ticket
```

The matrix uses the latest patch release in each Django series. List the
configured environments with `tox list -d --no-desc`.

Tests use an in-memory SQLite database and configure multiple ticket sequences
in `ticketing/tests/settings.py`. `tox.ini` defines the test matrix; GitHub
Actions discovers it with `tox list -d --no-desc` and runs every combination
and the Ruff checks on pushes and pull requests. Add or remove environments
in `tox.ini` to update both local and CI runs. CI infers the Python version
from each environment's `py<major><minor>` prefix (for example, `py315`).

The MySQL environments cover MySQL 8.4 (the minimum supported version) and
26.10 with each supported Django series. CI derives the MySQL service image
from the `-mysql-<version>` suffix in `tox.ini`.

For a local MySQL run, provide a disposable database server and credentials
for a user that can create and drop test databases:

```bash
export TICKETING_TEST_DB_USER=root
export TICKETING_TEST_DB_PASSWORD=ticketing-tests
export TICKETING_TEST_DB_PORT=3384
tox -e py315-django61-mysql-8.4
```

The host defaults to `127.0.0.1`; override it with `TICKETING_TEST_DB_HOST`.
Django creates and drops `test_ticketing`; set `TICKETING_TEST_DB_NAME` to
change the base database name. To run the complete matrix against multiple
local MySQL servers, use `TICKETING_TEST_MYSQL_8_4_PORT` and
`TICKETING_TEST_MYSQL_26_10_PORT` to select a port for each version.

Format all Python code and check lint and formatting locally with:

```bash
tox -e format
tox -e lint
```


## License

Uses the [MIT][mit] license.


[flickr]: http://code.flickr.com/blog/2010/02/08/ticket-servers-distributed-unique-primary-keys-on-the-cheap/
[pypi]: http://pypi.python.org/pypi/django-ticketing/
[mit]: http://opensource.org/licenses/MIT
