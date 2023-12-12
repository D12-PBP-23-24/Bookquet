from django.urls import path
from authentication.views import register, login, show_json, logout

app_name = 'authentication'

urlpatterns = [
    path('register/', register,  name='register'),
    path('login/', login, name='login'),
    path('json/', show_json, name='show_json'), 
    path('logout/', logout, name='logout'),
]