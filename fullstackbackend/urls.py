from django.contrib import admin
from django.urls import path
from app.views import get_job, get_tag, filter_tag

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getjob/', get_job),
    path('gettag/', get_tag),
    path('filtertag/', filter_tag),
]
