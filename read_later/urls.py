from django.urls import path
from . import views

app_name = "read_later"

urlpatterns = [
    path('', views.all_list, name="all_list"),
    # path('read/', views.read_later_list, name="read_later_list"),
    # path('read/<str:priority>', views.read_later_list2, name="read_later_list"),
    path('read/', views.read_later_list, name="read_later_list"),
    path('read/json/', views.read_later_list_json, name="read_later_list_json"),
    path('add-to-read-later/<int:book_id>/', views.add_to_read_later, name='add_to_read_later'),
    # path('remove_from_read_later/<int:entry_id>/', views.remove_from_read_later, name='remove_from_read_later'),
    path('delete_item_ajax/<int:item_id>/', views.delete_item_ajax, name='delete_item_ajax'),

    path('register/', views.register, name='register'), #sesuaikan dengan nama fungsi yang dibuat
    path('login/', views.login_user, name='login'), #sesuaikan dengan nama fungsi yang dibuat
    path('logout/', views.logout_user, name='logout'),
]