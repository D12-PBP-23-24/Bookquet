from django.urls import path
from main.views import show_main, get_books, get_book_json, find_book, register, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path("", show_main, name='show_main'),
    path("get-book", get_book_json, name="get_book_json"),
    path("api/books", get_books, name="get_books"),
    path("find-book", find_book, name="find_book"),
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]