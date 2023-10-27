from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField()

class Profile(User):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.TextField(null=True, blank=True)
    phone = models.IntegerField()
    age = models.IntegerField()
    region = models.TextField()