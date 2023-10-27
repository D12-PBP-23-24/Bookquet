from django.db import models
from django.contrib.auth.models import User

class UserProfile(User):
    nickname = models.TextField(null=True, blank=True)
    phone = models.IntegerField()
    age = models.IntegerField()
    region = models.TextField()

