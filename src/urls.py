from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

def greetings(request):
    program = request.GET.get('program', 'program')
    if program == 'error':
        1 / 0
    return HttpResponse(f"Greetings, {program}!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", greetings, name="greetings"),
]
