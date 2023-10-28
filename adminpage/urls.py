from django.urls import path
from adminpage.views import show_main, get_profile_json, edit_profile_ajax
from . import views

app_name = 'adminpage'

urlpatterns = [
    path("", show_main, name='show_main'),
    path('manage_quote_of_the_day/', views.manage_quote_of_the_day, name='manage_quote_of_the_day'),
    path('edit_quote_of_the_day/', views.edit_quote_of_the_day, name='edit_quote_of_the_day'),
    path('get_profile_json/', get_profile_json, name='get_profile_json'),
    path('edit_profile_ajax/', edit_profile_ajax, name='edit_profile_ajax'),
]


