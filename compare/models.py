from django.db import models

# Create your models here.


class Searchs(models.Model):
    searchId = models.AutoField(primary_key=True)
    searchName = models.CharField(max_length=100)