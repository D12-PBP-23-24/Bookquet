from django.db import models
from django.conf import settings
import random
from django.contrib.auth.models import User


class Book(models.Model):
  title       = models.CharField(null=True, blank=True, max_length=255)
  author      = models.CharField(null=True, blank=True, max_length=255)
  description = models.TextField(null=True, blank=True)
  isbn        = models.IntegerField(null=True, blank=True)
  genres      = models.TextField(null=True, blank=True)
  cover_img   = models.TextField(null=True, blank=True)
  year        = models.IntegerField(null=True, blank=True)
  average_rate= models.FloatField(null=True, blank=True)
  user_rated  = models.IntegerField(null=True, blank=True)

class UserProfile(User):
  nickname = models.TextField(null=True, blank=True)
  phone = models.IntegerField()
  age = models.IntegerField()
  region = models.TextField()


class QuoteOfDay(models.Model):
    quote_text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.quote_text

# class Review(models.Model):
#   review = models.ForeignKey(Book, on_delete=models.CASCADE)
class SearchFeatureStatus(models.Model):
  enabled = models.BooleanField(default=True)
