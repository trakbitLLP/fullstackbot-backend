from app.models import Job
import requests
from bs4 import BeautifulSoup
import os
from celery import Celery

app = ""
if 'DB_NAME' in os.environ:
    app = Celery('tasks', broker='redis://redis-mw7h:10000')
else:
    app = Celery('tasks', broker='redis://localhost:6379')


def scrap_stackoverflow_pg_1():
    Job.objects.all().delete()
    URL = 'https://stackoverflow.com/jobs/full-stack-developer-jobs/'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    jobs_list = soup.find(class_='listResults')

    jobs_items = jobs_list.find_all(class_='grid--cell fl1')
    jobs_image_items = jobs_list.find_all('img', class_='w48 h48 bar-sm')

    company_image = None
    company_name = None
    job_title = None
    job_location = None
    job_link = None

    company_images = []

    for job_image_element in jobs_image_items:
        company_image = job_image_element["src"]
        company_images.append(company_image)

    for i, job_element in enumerate(jobs_items):
        tags = []
        job_title = job_element.find('a', class_='s-link stretched-link').text

        job_title_anchor = (job_element.find('a', class_='s-link stretched-link'))
        job_link = 'https://stackoverflow.com'+job_title_anchor['href']

        company_and_location = job_element.find('h3', class_='fc-black-700 fs-body1 mb4').text

        company_name = (company_and_location.split('•')[0]).strip()
        job_location = (company_and_location.split('•')[1]).strip()

        tags_element = job_element.find_all('a', class_='post-tag no-tag-menu')
        for tag in tags_element:
            tags.append(tag.text)

        Job(
          company_image=company_images[i-1],
          company_name=company_name,
          job_title=job_title,
          job_location=job_location,
          job_link=job_link,
          tags=tags,
        ).save()


def scrap_stackoverflow_pg_2():
    URL = 'https://stackoverflow.com/jobs/full-stack-developer-jobs?pg=2'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    jobs_list = soup.find(class_='listResults')

    jobs_items = jobs_list.find_all(class_='grid--cell fl1')
    jobs_image_items = jobs_list.find_all('img', class_='w48 h48 bar-sm')

    company_image = None
    company_name = None
    job_title = None
    job_location = None
    job_link = None

    company_images = []

    for job_image_element in jobs_image_items:
        company_image = job_image_element["src"]
        company_images.append(company_image)

    for j, job_element in enumerate(jobs_items):
        tags = []
        job_title = job_element.find('a', class_='s-link stretched-link').text

        job_title_anchor = (job_element.find('a', class_='s-link stretched-link'))
        job_link = 'https://stackoverflow.com'+job_title_anchor['href']

        company_and_location = job_element.find('h3', class_='fc-black-700 fs-body1 mb4').text

        company_name = (company_and_location.split('•')[0]).strip()
        job_location = (company_and_location.split('•')[1]).strip()

        tags_element = job_element.find_all('a', class_='post-tag no-tag-menu')
        for tag in tags_element:
            tags.append(tag.text)

        Job(
          company_image=company_images[j-1],
          company_name=company_name,
          job_title=job_title,
          job_location=job_location,
          job_link=job_link,
          tags=tags,
        ).save()


def scraper():
    scrap_stackoverflow_pg_1()
    scrap_stackoverflow_pg_2()
