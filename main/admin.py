from django.contrib import admin
from main.models import Book, UserProfile
from book_preview.models import Comment, Rate, Filter

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Rate)
admin.site.register(Filter)
