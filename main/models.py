from django.contrib.postgres.fields import ArrayField
from django.db import models

class Book(models.Model):
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255)
  description = models.TextField()
  genres =  ArrayField(models.CharField(max_length=255))
  publish_date = models.DateField()
  #will be updated in the next development