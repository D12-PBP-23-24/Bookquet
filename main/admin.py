from django.contrib import admin
from main.models import Book, UserProfile
from book_preview.models import Comment, Rate

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Rate)
from django.contrib import admin
from .models import QuoteOfDay

admin.site.register(QuoteOfDay)
