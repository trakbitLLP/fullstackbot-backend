from django.contrib import admin
from django.urls import path
from app.views import job, get_tag, filter_tag, admin_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getjob/', job),
    path('editjob/', job),
    path('gettag/', get_tag),
    path('filtertag/', filter_tag),
    path('adminlogin/', admin_login),
]
