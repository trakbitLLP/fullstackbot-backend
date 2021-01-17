
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.db import models

class Job(models.Model):
  company_image = models.TextField()
  company_name = models.CharField(max_length=400)
  job_title = models.CharField(max_length=400)
  job_location = models.CharField(max_length=400)
  job_link = models.CharField(max_length=400)
  job_post = models.CharField(
        max_length=400,
        default=str(datetime.today().strftime('%Y-%m-%d')))
  tags = ArrayField(
            models.CharField(max_length=400, blank=True),
            size=8)