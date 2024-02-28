from django.contrib import admin
from app.models import Year


class YearAdmin(admin.ModelAdmin):
    list_display = ['year']


admin.site.register(Year, YearAdmin)
