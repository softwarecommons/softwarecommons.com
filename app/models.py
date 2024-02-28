from django.db import models


class Year(models.Model):
    year = models.IntegerField()
    fair_share = models.IntegerField()

class Organization(models.Model):
    name = models.CharField(max_length=256)
    ndevs = models.IntegerField()
    img_src = models.URLField(default='')

class FairShare(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.IntegerField()
    paid = models.IntegerField(default=0)

class OpenSourceEcosystem(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    img_src = models.URLField(default='')

class OpenSourceProject(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    ecosystem = models.ForeignKey(OpenSourceEcosystem, on_delete=models.CASCADE)
    img_src = models.URLField(default='')

class OpenProductModel(models.Model):
    name = models.CharField(max_length=256)

class OpenProduct(models.Model):
    name = models.CharField(max_length=256)
    model = models.ForeignKey(OpenProductModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    img_src = models.URLField(default='')
