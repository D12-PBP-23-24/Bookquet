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
# print("SEEDINGGGGG")
# comment_cnt = 0
# for i in range(100):
#   for j in range(random.randint(0, 3)):
#     bid = random.randint(1, 100)
#     c = Comment(komentar="It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).", buku=Book.objects.get(pk=bid))
#     c.save()