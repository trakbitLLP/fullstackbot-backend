from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import Response
from app.models import Job, Tag
from django.db import connection
import json
from app.scraper import scraper
import os
from celery import Celery
from django_expiring_token.models import ExpiringToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


app = ""
if 'DB_NAME' in os.environ:
    app = Celery('tasks', broker='redis://redis-mw7h:10000')
else:
    app = Celery('tasks', broker='redis://localhost:6379')


@app.task(name="scrapper")
def scrap_task():
    scraper()


@api_view(['GET'])
def get_job(request):
    jobs = Job.objects.all()
    connection.close()
    job_list = []
    for job in jobs:
        job_list.append({
            "jobId": job.pk,
            "companyImage": job.company_image,
            "companyName": job.company_name,
            "jobTitle": job.job_title,
            "jobLink": job.job_link,
            "jobLocation": job.job_location,
            "jobContent": job.job_content,
            "tags": job.tags
        })
    return Response({"jobs": job_list})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_job(request):
    try:
        request_data = json.loads(json.dumps(request.data))
        tags = request_data.get('tags').split(",")
        Job(
            company_image=request_data.get('companyImage'),
            company_name=request_data.get('companyName'),
            job_title=request_data.get('jobTitle'),
            job_location=request_data.get('jobLocation'),
            job_link=request_data.get('jobLink'),
            job_content=request_data.get('jobContent'),
            tags=tags,
            automated=False
        ).save()
        return Response({"saved": 1})
    except:
        return Response({"saved": 0})


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def edit_job(request):
    try:
        request_data = json.loads(json.dumps(request.data))
        job = Job.objects.get(pk=request_data.get('jobId'))
        job.company_name = request_data.get('companyName')
        job.job_title = request_data.get('jobTitle')
        job.job_location = request_data.get('jobLocation')
        job.job_link = request_data.get('jobLink')
        job.tags = request_data.get('tags')
        job.save()
        return Response({"saved": 1})
    except Job.DoesNotExist:
        return Response({"saved": 0})


@api_view()
def get_tag(request):
    tags = Tag.objects.all()
    connection.close()
    tag_list = []
    for tag in tags:
        tag_list.append({
            "tag": tag.tag,
            "count": tag.count
        })
    return Response({"tags": tag_list})


@api_view(['POST'])
def filter_tag(request):
    filter_tag = (request.body).decode("utf-8")
    jobs = Job.objects.all()
    connection.close()
    job_list = []
    for job in jobs:
        for tag in job.tags:
            if tag == filter_tag:
                job_list.append({
                    "companyImage": job.company_image,
                    "companyName": job.company_name,
                    "jobTitle": job.job_title,
                    "jobLink": job.job_link,
                    "jobLocation": job.job_location,
                    "jobContent": job.job_content,
                    "tags": job.tags
                })
    return Response({"jobs": job_list})


@api_view(['POST'])
def admin_login(request):
    request_data = json.loads(json.dumps(request.data))
    email = request_data.get('email')
    password = request_data.get('password')
    token = 0
    loggedIn = 0
    try:
        user = User.objects.get(is_superuser=True, email=email)
        if user.check_password(password) is True:
            token, _ = ExpiringToken.objects.get_or_create(user=user)
            loggedIn = 1
    except User.DoesNotExist:
        print('User.DoesNotExist')
    return Response({
        "loggedIn": loggedIn,
        "token": token.key
    })
