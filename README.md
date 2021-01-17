# fullstackbot-backend

## setup
### create database
create database with name **fullstackjob** in **PostgreSQL**

### create tables
```
python manage.py makemigrations
python manage.py migrate
```
### start backend
```
python manage.py runserver
```
### start redis
```
redis-server
```
### start worker
```
python -m celery -A fullstackbackend worker -l info
```
### start background job - for scraping jobs from stackoverflow.com
```
python -m celery -A fullstackbackend beat -l info
```
