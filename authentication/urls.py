from django.urls import path
from authentication.views import login, show_json, logout

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('json/', show_json, name='show_json'), 
    path('logout/', logout, name='logout'),
]