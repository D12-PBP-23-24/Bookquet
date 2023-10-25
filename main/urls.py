from django.urls import path
from main.views import show_main, get_books

app_name = 'main'

urlpatterns = [
    path("", show_main, name='show_main'),
    path("api/books", get_books, name="get_books")
]