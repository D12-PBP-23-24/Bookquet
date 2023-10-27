from django.urls import path
from adminpage.views import show_main, add_book, edit_book, delete_book
from adminpage.views import show_xml, show_json, show_xml_by_id, show_json_by_id
from adminpage.views import get_book_json, get_books


app_name = 'adminpage'

urlpatterns = [
    path('add-book', add_book, name='add_book'),
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
    path('edit-book/<int:id>', edit_book, name='edit_book'),
    path('delete/<int:id>', delete_book, name='delete_book'),
    path("get-book", get_book_json, name="get_book_json"),
    path("api/books", get_books, name="get_books")
]