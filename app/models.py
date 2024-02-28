from django.db import models


class Year(models.Model):
    year = models.IntegerField()
    fair_share = models.IntegerField()
