from rest_framework.decorators import api_view
from rest_framework.views import Response
from app.models import Job
from django.db import connection
import json
from app.scrapper import scrapper
import os
from celery import Celery

app = ""
if 'DB_NAME' in os.environ:
    app = Celery('tasks', broker='redis://trakbit-cbqq:10000')
else:
    app = Celery('tasks', broker='redis://localhost:6379')


@app.task(name="scrapper")
def scrap_task():
    scrapper()


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
