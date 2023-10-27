from django.urls import path
from authentication.views import register #sesuaikan dengan nama fungsi yang dibuat
from authentication.views import login_user, show_main #sesuaikan dengan nama fungsi yang dibuat

app_name = 'authentication'

urlpatterns = [
    path("", show_main, name='show_main'),
    path('register/', register, name='register'), #sesuaikan dengan nama fungsi yang dibuat
    path('login/', login_user, name='login'),
]