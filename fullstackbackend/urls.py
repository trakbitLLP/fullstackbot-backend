from django.contrib import admin
from django.urls import path
from app.views import get_job

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getjob/', get_job)
]
