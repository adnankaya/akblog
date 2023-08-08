
# akblog (Adnan Kaya Blog) app

## Installations

```bash
# clone the project
git clone https://github.com/adnankaya/pytrinfo.git
# go to project directory
cd pytrinfo
# create venv instance named as env
python3.11 -m venv env
# for linux/macos users
source env/bin/activate
# for windows users
.\env\Scripts\activate
# install packages
pip install -r requirements/dev.txt
# DOCKER
# docker exec -it postgres-bb psql -U dbuser
# create database db_pytrinfo;
# Migrate files
python manage.py migrate
# [Optional] make migrations if necessary
python manage.py makemigrations <app-name>
python manage.py migrate
# [DEVELOPMENT] init all command
python manage.py init_all
# run project for development mode
python manage.py runserver --settings=src.settings.dev
# run project for production mode
python manage.py runserver --settings=src.settings.prod
# run project for test mode
python manage.py runserver --settings=src.settings.settings_for_test
```
## Static Files
```
python manage.py collectstatic
```

## Internationalization
```
python manage.py makemessages --all --ignore=venv
python manage.py compilemessages
```

---
## Flat Pages
### Terms of page
- Admin site /terms-of-use/ must be added


## Technical Notes

1. Find and remove migration files
```bash
find . -path "*/migrations/*.py" -not -path "./venv/*" -not -name "__init__.py" -delete
```

## Load Test
```bash
# run gunicorn with 4 workers
gunicorn core.wsgi:application -w 4

# new terminal apache bench
ab -n 100 -c 10 http://127.0.0.1:8000/
# This will simulate 100 connections over 10 concurrent threads. That's 100 requests, 10 at a time.
```