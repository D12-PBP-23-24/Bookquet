from django.urls import path
from . import views

app_name = "read_later"

urlpatterns = [
    path('', views.read_later_list, name="read_later_list"),
    path('read/json/', views.read_later_list_json, name="read_later_list_json"),
    path('add-to-read-later/<int:book_id>/', views.add_to_read_later, name='add_to_read_later'),
    path('delete_item_ajax/<int:item_id>/', views.delete_item_ajax, name='delete_item_ajax'),
    path('adjust_priority_ajax/<int:item_id>/', views.adjust_priority_ajax, name='adjust_priority_ajax'),
    path('add-to-read-later2/<int:book_id>/', views.add_to_read_later2, name='add_to_read_later2'),
]