from django.urls import path
from dashboard.views import filter_books_view, get_profile_json, get_rated_books_json, show_dashboard, edit_profile_ajax, show_json , show_xml, get_profile, update_profile_flutter

app_name = 'dashboard'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
    path('get_profile/', get_profile, name='get_profile'),
    path('get_profile_json/', get_profile_json, name='get_profile_json'),
    path('edit_profile_ajax/', edit_profile_ajax, name='edit_profile_ajax'),
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'), 
    path('get_rated_books_json/', get_rated_books_json, name='get_rated_books_json'),
    path('filter_books/', filter_books_view, name='filter_books'),
     path('update_profile_flutter/', update_profile_flutter, name='update_profile_flutter'),
]