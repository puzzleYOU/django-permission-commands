# django-permission-commands
Django management commands for ruling groups and permissions based
on `django.contrib.auth`.

## Set up

First, please install `python3` and `python3-venv`.
Then set up your virtualenv-based test environment as follows:

- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 setup.py install`
- `./manage.py collectstatic`
- `./manage.py migrate`
- `./manage.py createsuperuser`
- `./manage.py loaddata sample_app/fixtures.json`

After having initially set up the virtual environment, it's sufficient
to only run `source .venv/bin/activate` the next times, obviously.

Within the virtual environment, `./manage.py` should list `grantpermissions`
and `revokepermissions` as available commands.

It's also rational to create an admin user via `./manage.py createsuperuser`.

## Trying out the commands

You can start the Django debug server using `./manage.py runserver`.
After that, you can log in into the Django administration using the
credentials of your previously created super user.
There you can create new users and try out their permissions after
managing the permissions via `grantpermissions` / `revokepermissions`.
