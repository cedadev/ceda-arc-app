# arcapp

A simple django application for working with ARC-CE. Written to demo functionality at CEDA.

See:

https://docs.google.com/document/d/19ioTHXzFqJAuD28_CG8wX5me-sG579vA3hIXBRXgooI/edit

## Installation

```
$ sudo su 
$ cd /usr/local
$ mkdir arc-app
$ cd arc-app/

$ git clone https://agstephens@github.com/cedadev/ceda-arc-app
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r ceda-arc-app/requirements.txt

$ cp arcproj/settings_local.py.tmpl arcproj/settings_local.py 
```

In the `settings_local.py` file make up a secret key string (about 30 characters)
and add the hostname to the `ALLOWED_HOSTS` list.

## Set up database

```
$ mkdir db
$ python manage.py migrate
```

## Start service

```
$ python manage.py runserver localhost:8000

## Testing

Try:

`$ py.test -k arcapp`
