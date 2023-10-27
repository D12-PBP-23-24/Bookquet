from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from main.models import Book

# class ReadLaterBooks(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
#     class Meta:
#         unique_together = ['user', 'book']

class ReadLaterBooks(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    
    class Meta:
        unique_together = ['user', 'book']
