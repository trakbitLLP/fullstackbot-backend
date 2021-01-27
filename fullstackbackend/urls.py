from django.contrib import admin
from django.urls import path
from app.views import (
    get_job,
    edit_job,
    get_tag,
    filter_tag,
    admin_login,
    add_job
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getjob/', get_job),
    path('editjob/', edit_job),
    path('addjob/', add_job),
    path('gettag/', get_tag),
    path('filtertag/', filter_tag),
    path('adminlogin/', admin_login),
]
