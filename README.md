
# Full-Stack Developer Job Board ([Back-End](https://github.com/TrakBit/fullstackbot-backend)/[Front-End](https://github.com/TrakBit/FullStackBot))
[![FullStackBot](https://dev-to-uploads.s3.amazonaws.com/i/wyo7ixlmesq0otbwpjat.jpg)](https://www.fullstackbot.com/)

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
# Learn how to take this job board live here: 
[![Deploy Django App](https://firebasestorage.googleapis.com/v0/b/squarespace-chat.appspot.com/o/images%2Fcover.jpg?alt=media&token=f4cd35d5-ef54-4405-a607-498112512713)](https://codetolive.carrd.co/)
