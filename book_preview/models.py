from django.db import models
from django.contrib.auth.models import User
from main.models import Book
from django.conf import settings

class Comment(models.Model):
  komentar    = models.TextField(null=True)
  buku        = models.ForeignKey(Book, on_delete=models.CASCADE)
  user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class RatedBook(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)




