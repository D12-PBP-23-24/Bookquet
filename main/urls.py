from django.urls import path
from main.views import show_main, get_books, get_book_json, find_book, register, login_user, logout_user, read_later_book, manage_quote_of_the_day, edit_quote_of_the_day
from . import views

app_name = 'main'

urlpatterns = [
    path("", show_main, name='show_main'),
    path("get-book", get_book_json, name="get_book_json"),
    path("api/books", get_books, name="get_books"),
    path("find-book", find_book, name="find_book"),
    path('register/', register, name='register'), 
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('read-later/add-to-read-later/<int:book_id>/', read_later_book, name="read_later_book"),
    path('manage_quote_of_the_day/', views.manage_quote_of_the_day, name='manage_quote_of_the_day'),
    path('edit_quote_of_the_day/', views.edit_quote_of_the_day, name='edit_quote_of_the_day'),
]


