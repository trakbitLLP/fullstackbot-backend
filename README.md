# fullstackbot-backend

## setup
### create database
create database with name **fullstackjob** in **PostgreSQL**

### Install python packages
```
pip install -r requirements.txt
```
### Create tables
```
python manage.py makemigrations
python manage.py migrate
```
### Start backend
```
python manage.py runserver
```
### Start redis
```
redis-server
```
### Start worker
```
python -m celery -A fullstackbackend worker -l info
```
### Start background job - for scraping jobs from stackoverflow.com
```
python -m celery -A fullstackbackend beat -l info
```
