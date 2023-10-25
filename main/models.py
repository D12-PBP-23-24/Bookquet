from django.db import models

class Book(models.Model):
  title       = models.CharField(null=True, blank=True, max_length=255)
  author      = models.CharField(null=True, blank=True, max_length=255)
  description = models.TextField(null=True, blank=True)
  isbn        = models.IntegerField(null=True, blank=True)
  genres      = models.TextField(null=True, blank=True)
  cover_img   = models.TextField(null=True, blank=True)
  year        = models.IntegerField(null=True, blank=True)