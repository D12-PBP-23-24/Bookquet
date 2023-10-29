from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(User):
    nickname = models.TextField(null=True, blank=True)
    phone = models.IntegerField()
    age = models.IntegerField()
    region = models.TextField()
    user_ptr = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, related_name='admin_userprofile')

class QuoteOfDay(models.Model):
    quote_text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.quote_text