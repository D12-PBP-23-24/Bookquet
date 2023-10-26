from django.contrib import admin
from main.models import Book, Comment, Rate, UserProfile

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(UserProfile)