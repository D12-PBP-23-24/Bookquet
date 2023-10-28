from django.urls import path
from dashboard.views import get_profile_json, show_dashboard, edit_profile_ajax
from . import views
app_name = 'dashboard'

urlpatterns = [
    path('', show_dashboard, name='show_dashboard'),
    path('get_profile_json/', get_profile_json, name='get_profile_json'),
    path('edit_profile_ajax/', edit_profile_ajax, name='edit_profile_ajax'),

    path('register/',views.register,name = 'register'),
    path('login/',views.login_user,name = 'login'),
    path('logout/',views.logout_user,name = 'logout'),
]