from django.contrib import admin
from app import models


class YearAdmin(admin.ModelAdmin):
    list_display = ['year']
admin.site.register(models.Year, YearAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.Organization, OrganizationAdmin)

class FairShareAdmin(admin.ModelAdmin):
    list_display = ['organization', 'year']
admin.site.register(models.FairShare, FairShareAdmin)

class OpenSourceEcosystemAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.OpenSourceEcosystem, OpenSourceEcosystemAdmin)

class OpenSourceProjectAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.OpenSourceProject, OpenSourceProjectAdmin)

class OpenProductModelAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.OpenProductModel, OpenProductModelAdmin)

class OpenProductAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(models.OpenProduct, OpenProductAdmin)
