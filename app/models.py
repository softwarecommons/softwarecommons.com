from django.db import models


class Year(models.Model):
    year = models.IntegerField()
    fair_share = models.IntegerField()

    def __str__(self):
       return str(self.year)

class Organization(models.Model):
    name = models.CharField(max_length=256)
    img_src = models.URLField(default='')

    def __str__(self):
       return self.name

class FairShare(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    ndevs = models.IntegerField(null=True)
    paid = models.IntegerField(default=0)

    def __str__(self):
       return str(self.year)

class OpenSourceEcosystem(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    img_src = models.URLField(default='')

    def __str__(self):
       return self.name

class OpenSourceProject(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    ecosystem = models.ForeignKey(OpenSourceEcosystem, on_delete=models.CASCADE)
    img_src = models.URLField(default='')

    def __str__(self):
       return self.name

class OpenProductModel(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
       return self.name

class OpenProduct(models.Model):
    name = models.CharField(max_length=256)
    model = models.ForeignKey(OpenProductModel, on_delete=models.CASCADE)
    owner = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    img_src = models.URLField(default='')

    def __str__(self):
       return self.name
