from django.urls import path
from main.views import show_main, get_books, get_book_json

app_name = 'adminpage'

urlpatterns = [
    path("", show_main, name='show_main'),
    #path("get-book", get_book_json, name="get_book_json"),
    #path("api/books", get_books, name="get_books")
]