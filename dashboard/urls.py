from django.urls import path
from dashboard.views import get_profile_json, show_main, edit_profile_ajax

app_name = 'dashboard'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('get_profile_json/', get_profile_json, name='get_profile_json'),
    path('edit_profile_ajax/', edit_profile_ajax, name='edit_profile_ajax'),

]