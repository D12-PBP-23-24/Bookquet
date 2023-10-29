from django.urls import path
from dashboard.views import get_profile_json, show_dashboard, edit_profile_ajax, show_json , show_xml

app_name = 'dashboard'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
    path('get_profile_json/', get_profile_json, name='get_profile_json'),
    path('edit_profile_ajax/', edit_profile_ajax, name='edit_profile_ajax'),
    path('xml/', show_xml, name='show_xml'), 
    path('json/', show_json, name='show_json'), 
]