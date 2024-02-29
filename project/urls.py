from django.contrib import admin
from django.urls import path
from django_aspen import view

urlpatterns = [path('admin/', admin.site.urls), path("", view)]
