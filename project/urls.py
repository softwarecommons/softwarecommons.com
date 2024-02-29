from django.contrib import admin
from django.urls import path, re_path
from django_aspen import view

urlpatterns = [path('admin/', admin.site.urls), re_path(".*", view)]
