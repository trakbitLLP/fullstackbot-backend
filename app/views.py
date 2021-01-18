from rest_framework.decorators import api_view
from rest_framework.views import Response
from app.models import Job, Tag
from django.db import connection
import json
from app.scraper import scraper
import os
from celery import Celery


app = ""
if 'DB_NAME' in os.environ:
    app = Celery('tasks', broker='redis://redis-mw7h:10000')
else:
    app = Celery('tasks', broker='redis://localhost:6379')


@app.task(name="scrapper")
def scrap_task():
    scraper()


@api_view(['POST'])
def post_job(request):
    Job.objects.all().delete()
    request_data = json.loads(json.dumps(request.data))
    for company in request_data:
        Job(
            company_image=company.get('companyImage'),
            company_name=company.get('companyName'),
            job_title=company.get('jobTitle'),
            job_location=company.get('jobLocation'),
            job_link=company.get('jobLink'),
            tags=company.get('tags'),
        ).save()
    connection.close()
    return Response({"hello": "world"})


@api_view()
def get_job(request):
    jobs = Job.objects.all()
    connection.close()
    job_list = []
    for job in jobs:
        job_list.append({
          "companyImage": job.company_image,
          "companyName": job.company_name,
          "jobTitle": job.job_title,
          "jobLink": job.job_link,
          "jobLocation": job.job_location,
          "tags": job.tags
        })
    return Response({"jobs": job_list})


@api_view()
def get_tag(request):
    tags = Tag.objects.all()
    connection.close()
    tag_list = []
    for tag in tags:
        tag_list.append(tag.tag)
    return Response({"tags": tag_list})


@api_view(['POST'])
def filter_tag(request):
    filter_tag = (request.body).decode("utf-8")
    jobs = Job.objects.all()
    connection.close()
    job_list = []
    for job in jobs:
        tags = job.tags
        for tag in tags:
            if tag in filter_tag:
                job_list.append({
                    "companyImage": job.company_image,
                    "companyName": job.company_name,
                    "jobTitle": job.job_title,
                    "jobLink": job.job_link,
                    "jobLocation": job.job_location,
                    "tags": job.tags
                })
    return Response({"jobs": job_list})
